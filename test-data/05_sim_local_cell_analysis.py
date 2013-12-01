import sys, os, random

cwd = os.getcwd().split(os.sep)
cwd[-1] = 'dose'
cwd = os.sep.join(cwd)
sys.path.append(cwd)

import analytics
import database_calls

database_filename = "case_study_01.db"
outputfile = 'sim05_resultV2.csv'
outputfile = open(outputfile, 'w')
dbpath = os.getcwd().split(os.sep)
dbpath[-1] = 'examples'
dbpath = os.sep.join(dbpath)
dbpath = os.sep.join([dbpath, 'Simulations', database_filename])
(con, cur) = database_calls.connect_database(dbpath, None)
starting_time = database_calls.db_list_simulations(cur)[2][0]
pop_name = database_calls.db_list_population_name(cur, starting_time)[0]

locations = []
for x in xrange(5):
    for y in xrange(5):
            locations.append((x,y,0));

def get_chromosomes_by_location(starting_time, pop_name, generation):
    organisms = database_calls.db_reconstruct_organisms(cur, starting_time, pop_name, generation)
    organism_chromosomes = {}
    for location in locations:
        organism_chromosomes[location] = []
        for organism in organisms:
            if organism.status['location'] == location:
                organism_chromosomes[location].append(organism.genome[0].sequence)
    return organism_chromosomes

header = [str(locations[i]).replace(", ","-") for i in xrange(len(locations))]
header = ['Generation'] + header
outputfile.write(','.join(header) + '\n')

for generation in range(1, 1001):
    chromo_db = get_chromosomes_by_location(starting_time, pop_name, generation)
    result = [str(generation)]
    for location in locations:
        genetic_distance_list = []
        for chromosome in chromo_db[location]:
            random_chromosome = random.choice(chromo_db[location])
            genetic_distance_list.append(analytics.hamming_distance(random_chromosome, chromosome))
        average_distance = float(sum(genetic_distance_list))/len(genetic_distance_list)
        result.append(str(average_distance))
    outputfile.write(','.join(result) + '\n')
    print ','.join(result)
