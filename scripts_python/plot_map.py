import fiona
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import shape, Polygon, MultiPolygon
from time import time, sleep
import redis
from tw_streamer.engine.enum_vals import Constants
from matplotlib import cm

print(f"Matplotlib version: {matplotlib.__version__}")

# plt.switch_backend('agg')


geometries = {
    'AL': None,
    'AZ': None,
    'AR': None,
    'CA': None,
    'CO': None,
    'CT': None,
    'DE': None,
    'FL': None,
    'GA': None,
    'ID': None,
    'IL': None,
    'MS': None,
    'NJ': None,
    'PA': None,
    'TX': None,
    'WI': None
}

shape_file = fiona.open("../data/tl_2017_us_state.shp")

t = time()
for collection in iter(shape_file):
    #
    # Each collection has four keys ['type', 'id', 'properties', 'geometry']
    state_abbreviation = collection['properties']['STUSPS']

    # Shapely Polygon object
    state_geometry = shape(collection['geometry'])
    if isinstance(state_geometry, Polygon):
        state_geometry = MultiPolygon([state_geometry])

    # State name
    state_name = collection['properties']['NAME']

    #
    #
    #
    #
    if state_abbreviation in geometries.keys():
        geometries[state_abbreviation] = state_geometry

    # fig, ax = plt.subplots(figsize=(12, 9))
    #
    # for geom in state_geometry.geoms:
    #     x, y = geom.exterior.coords.xy
    #     ax.fill(x, y, alpha=0.5, color='C2', edgecolor='k')
    #     # ax.plot(x, y, '-k')
    #     ax.set_title(f"{state_name} : {state_abbreviation}")
    #
    # plt.show()
print(f"Loaded all the geometries in {time() - t} seconds")


t = time()

plt.ion()
fig, ax = plt.subplots(figsize=(12, 9))

# for state_abbreviation, state_geometry in geometries.items():
#     for geom in state_geometry.geoms:
#         x, y = geom.exterior.coords.xy
#         ax.fill(x, y, alpha=0.5, color='C2', edgecolor='k')
#         # ax.plot(x, y, '-k')
#         ax.set_title(f"{state_abbreviation}")
# print(f"Plotted within {time() - t} seconds")
# # fig.canvas.draw()
# plt.pause(0.01)


colors = ['r', 'g', 'b', 'm', 'y', 'k']

# Get target word
redis_client = redis.Redis(host='localhost', port=6379, db=0)


counters = dict()


# cm = LinearSegmentedColormap.from_list('Goerge', [(1, 0, 0), (0, 1, 0), (0, 0, 1)], N=100)
cc = cm.get_cmap('Reds')


while True:
    target_word = redis_client.get(Constants.TARGET_WORD_KEY).decode('utf-8')

    # Get all counters
    for state_abbreviation in geometries.keys():
        counter = redis_client.get(f'USA:{state_abbreviation}:CITY:{target_word}')

        try:
            counter = int(counter)
        except (ValueError, TypeError):
            counter = 0

        counters[state_abbreviation] = counter

    # Generate color maps
    min_counter = min(counters.values())
    max_counter = max(counters.values())
    # print(min_counter, max_counter)

    # Plot states
    plt.cla()
    for state_abbreviation, state_geometry in geometries.items():

        # Scale to [0, 1] range
        counter_scaled = (counters[state_abbreviation] - min_counter) / (max_counter - min_counter)

        # print(counter_scaled)

        color = cc(counter_scaled)
        # print(state_abbreviation, color)

        for geom in state_geometry.geoms:
            x, y = geom.exterior.coords.xy
            ax.fill(x, y, color=color, edgecolor='k')
            # ax.plot(x, y, '-k')
            ax.set_title(f"{state_abbreviation}: {target_word}")
    print(f"Plotted within {time() - t} seconds")

    # fig.canvas.draw()
    plt.pause(0.01)

    sleep(5)
