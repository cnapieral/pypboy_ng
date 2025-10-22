import xmltodict
import requests
import numpy
from numpy.fft import fft
from math import log10
import math
import pygame
import os

class Maps(object):
    nodes = {}
    ways = []
    tags = []
    origin = None
    width = 0
    height = 0
    
    SIG_PLACES = 3
    GRID_SIZE = 0.001
    
    def __init__(self, *args, **kwargs):
        super(Maps, self).__init__(*args, **kwargs)
        self.nodes = {}  # ← NEU: Dict für Nodes (ID → Node-Daten)
        self.tags = []   # ← NEU: Liste für POIs (Lat, Lon, Name, Amenity)
        self.ways = []   # ← NEU: Liste für Straßen (Waypoints-Listen)
    
    def float_floor_to_precision(self, value, precision):
        for i in range(precision):
            value *= 10
        value = math.floor(value)
        for i in range(precision):
            value /= 10
        return value
    
    def fetch_grid(self, coords):
        lat = coords[0]
        lng = coords[1]
        
        return self.fetch_area([
            lat - self.GRID_SIZE,
            lng - self.GRID_SIZE,
            lat + self.GRID_SIZE,
            lng + self.GRID_SIZE
        ])
    
    def fetch_area(self, bounds):
        self.width = (bounds[2] - bounds[0]) / 2
        self.height = (bounds[3] - bounds[1]) / 2
        self.origin = (
            bounds[0] + self.width,
            bounds[1] + self.height
        )
        url = "http://www.openstreetmap.org/api/0.6/map?bbox=%f,%f,%f,%f" % (
            bounds[0],
            bounds[1],
            bounds[2],
            bounds[3]
        )
        #For testing
        #url = "http://www.openstreetmap.org/api/0.6/map?bbox=13.4,52.5,13.41,52.51" #Berlin
        print("[Fetching maps... (%f, %f) to (%f, %f)]" % (
            bounds[0],
            bounds[1],
            bounds[2],
            bounds[3]
        ))
        while True:
            try:
                response = requests.get(url)
            except:
                pass
            else:
                break
        map_data = response.text.encode('UTF-8')
        # Write to cache file
        f = open("map.cache", "wb")
        f.write(map_data)
        f.close()
        self.display_map(map_data)
    
    def load_map_coordinates(self, coords, range):
        return self.load_map((
            coords[0] - range,
            coords[1] - range,
            coords[0] + range,
            coords[1] + range
        ))
    
    def load_map(self, bounds):
        self.width = (bounds[2] - bounds[0]) / 2
        self.height = (bounds[3] - bounds[1]) / 2
        self.origin = (
            bounds[0] + self.width,
            bounds[1] + self.height
        )

        cache_file = 'map.cache'

        #TODO check if map.cache exists
        # Prüfe und erstelle leere Cache bei Bedarf
        if not os.path.exists(cache_file):
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write('')
            print(f"[Created empty cache: {cache_file}]")
        with open('map.cache', 'r') as mapcache:
            map_data = mapcache.read()
        self.display_map(map_data)

# def load_map(self, bounds):
#     self.width = (bounds[2] - bounds[0]) / 2
#     self.height = (bounds[3] - bounds[1]) / 2
#     self.origin = (
#         bounds[0] + self.width,
#         bounds[1] + self.height
#     )
    
#     cache_file = 'map.cache'
    
#     # TODO umgesetzt: Prüfe, ob Cache existiert
#     if os.path.exists(cache_file):
#         try:
#             with open(cache_file, 'r', encoding='utf-8') as mapcache:
#                 map_data = mapcache.read().strip()  # Strip für sauberes XML
#             if map_data:
#                 print(f"[Loaded cached map from {cache_file}]")
#                 self.display_map(map_data)
#             else:
#                 print(f"[Empty cache {cache_file} – fetching new]")
#                 self.fetch_area(bounds)  # Fallback: Neu laden
#         except (IOError, UnicodeDecodeError) as e:
#             print(f"[Cache read error: {e} – fetching new]")
#             self.fetch_area(bounds)
#     else:
#         print(f"[No cache {cache_file} found – fetching new]")
#         self.fetch_area(bounds)  # Neu laden und cachen (via fetch_area)

    def display_map(self, map_data):
        osm_dict = xmltodict.parse(map_data)
        try:
            for node in osm_dict['osm']['node']:
                self.nodes[node['@id']] = node
                if 'tag' in node:
                    for tag in node['tag']:
                        try:
                            # Named Amenities
                            if tag["@k"] == "name":
                                for tag2 in node['tag']:
                                    if tag2["@k"] == "amenity":
                                        amenity = tag2["@v"]
                                        self.tags.append((float(node['@lat']), float(node['@lon']), tag["@v"], amenity))
                            # Personal Addresses - Removed
                            #if tag["@k"] == "addr:housenumber":
                            #      for t2 in node['tag']:
                            #              if t2["@k"] == "addr:street":
                            #                      self.tags.append((float(node['@lat']), float(node['@lon']),tag["@v"]+" "+t2["@v"]))
                        except Exception as e:
                            pass
            
            for way in osm_dict['osm']['way']:
                waypoints = []
                for node_id in way['nd']:
                    node = self.nodes[node_id['@ref']]
                    waypoints.append((float(node['@lat']), float(node['@lon'])))
                self.ways.append(waypoints)
        except Exception as e:
            print(e)
    
    def fetch_by_coordinate(self, coords, range):
        return self.fetch_area((
            coords[0] - range,
            coords[1] - range,
            coords[0] + range,
            coords[1] + range
        ))
    
    def transpose_ways(self, dimensions, offset, flip_y=True):
        width = dimensions[0]
        height = dimensions[1]
        w_coef = width / self.width / 2
        h_coef = height / self.height / 2
        transways = []
        for way in self.ways:
            transway = []
            for waypoint in way:
                lat = waypoint[1] - self.origin[0]
                lng = waypoint[0] - self.origin[1]
                wp = [
                    (lat * w_coef) + offset[0],
                    (lng * h_coef) + offset[1]
                ]
                if flip_y:
                    wp[1] *= -1
                    wp[1] += offset[1] * 2
                transway.append(wp)
            transways.append(transway)
        return transways
    
    def transpose_tags(self, dimensions, offset, flip_y=True):
        width = dimensions[0]
        height = dimensions[1]
        w_coef = width / self.width / 2
        h_coef = height / self.height / 2
        transtags = []
        for tag in self.tags:
            lat = tag[1] - self.origin[0]
            lng = tag[0] - self.origin[1]
            wp = [
                tag[2],
                (lat * w_coef) + offset[0],
                (lng * h_coef) + offset[1],
                tag[3]
            ]
            if flip_y:
                wp[2] *= -1
                wp[2] += offset[1] * 2
            transtags.append(wp)
        return transtags

class SoundSpectrum:
    """
    Obtain the spectrum in a time interval from a sound file.
    """
    
    left = None
    right = None
    
    def __init__(self, filename, force_mono=False):
        """
        Create a new SoundSpectrum instance given the filename of
        a sound file pygame can read. If the sound is stereo, two
        spectra are available. Optionally mono can be forced.
        """
        # Get playback frequency
        nu_play, format, stereo = pygame.mixer.get_init()
        self.nu_play = 1./nu_play
        self.format = format
        self.stereo = stereo
        
        # Load sound and convert to array(s)
        sound = pygame.mixer.Sound(filename)
        a = pygame.sndarray.array(sound)
        a = numpy.array(a)
        if stereo:
            if force_mono:
                self.stereo = 0
                self.left = (a[:,0] + a[:,1])*0.5
            else:
                self.left = a[:,0]
                self.right = a[:,1]
        else:
            self.left = a
    
    def get(self, data, start, stop):
        """
        Return spectrum of given data, between start and stop
        time in seconds.
        """
        duration = stop-start
        # Filter data
        start = int(start/self.nu_play)
        stop = int(stop/self.nu_play)
        N = stop - start
        data = data[start:stop]
        
        # Get frequencies
        frequency = numpy.arange(N/2)/duration
        
        # Calculate spectrum
        spectrum = fft(data)[1:1+N/2]
        power = (spectrum).real
        
        return frequency, power
    
    def get_left(self, start, stop):
        """
        Return spectrum of the left stereo channel between
        start and stop times in seconds.
        """
        return self.get(self.left, start, stop)
    
    def get_right(self, start, stop):
        """
        Return spectrum of the left stereo channel between
        start and stop times in seconds.
        """
        return self.get(self.right, start, stop)
    
    def get_mono(self, start, stop):
        """
        Return mono spectrum between start and stop times in seconds.
        Note: this only works if sound was loaded as mono or mono
        was forced.
        """
        return self.get(self.left, start, stop)

class LogSpectrum(SoundSpectrum):
    """
    A SoundSpectrum where the spectrum is divided into
    logarithmic bins and the logarithm of the power is
    returned.
    """
    
    def __init__(self, filename, force_mono=False, bins=20, start=1e2, stop=1e4):
        """
        Create a new LogSpectrum instance given the filename of
        a sound file pygame can read. If the sound is stereo, two
        spectra are available. Optionally mono can be forced.
        The number of spectral bins as well as the frequency range
        can be specified.
        """
        SoundSpectrum.__init__(self, filename, force_mono=force_mono)
        start = log10(start)
        stop = log10(stop)
        step = (stop - start)/bins
        self.bins = 10**numpy.arange(start, stop+step, step)
    
    def get(self, data, start, stop):
        """
        Return spectrum of given data, between start and stop
        time in seconds. Spectrum is given as the log of the
        power in logatithmically equally sized bins.
        """
        f, p = SoundSpectrum.get(self, data, start, stop)
        bins = self.bins
        length = len(bins)
        result = numpy.zeros(length)
        ind = numpy.array([int(x) for x in bins])  # Fixed: added proper conversion
        for i, bin_val in enumerate(bins):
            if i < len(ind) and ind[i] < len(p):
                result[i] = p[ind[i]]
        return result
