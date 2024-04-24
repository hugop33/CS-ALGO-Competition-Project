import sys, os, time
# pour lire un dictionnaire d'un fichier
import ast
# pour faire la statistique
import statistics, numpy
# pour verifier si une solution online traite toutes les tâches
import collections
# pour utiliser random, si besoin est
import random
import math
import copy

# -------------------------------------------------------------- #
# --------------------- Variables globales --------------------- #
# -------------------------------------------------------------- #

global fast_speed, sol_online # sol_online permet de consulter l'état de machines en cours de traitement

# la vitesse des machines rapides est toujours unitaire
fast_speed=1


# -------------------------------------------------------------- #
# --- Fonctions utilitaires - n'y touchez pas, les enfants ! --- #
# -------------------------------------------------------------- #

def val_sol(sigma, m, fast_nb, slow_speed, sol):
    load = []
    for machine in sol[:fast_nb]:
        load_machine = sum(machine)*fast_speed
        load.append(load_machine)
    for machine in sol[fast_nb:]:
        load_machine = sum(machine)*slow_speed
        load.append(load_machine)
    return max(load)

def verify_solution(sigma, sol):
    # applatir la solution online pour pouvoir la comparer avec sigma
    attributed_to_machines = [job for machine in sol for job in machine]
    if not collections.Counter(attributed_to_machines) == collections.Counter(sigma):
        print("Solution incompléte")
        exit

def mon_algo_est_deterministe():
    # par défaut l'algo est considéré comme déterministe
    # changez response = False dans le cas contraire
    response = False #False #True 
    return response 

##############################################################
# La fonction à completer pour la compétition
##############################################################

# La fonction à completer pour la compétition
def slow_fast_scheduling_online(sol_online, m, fast_nb, slow_speed, job):
    best_solution = None
    best_score = float('inf')
    jobs=[jobi for machine in sol_online for jobi in machine]
    high_value=False
    
    if len(jobs)>random.randint(6,10):
        tri=jobs[:]
        tri.sort(reverse=True)
        if tri[0]>=2*tri[1]:
            high_value=True
        
    if not jobs:
        sol_online[0].append(job)
        return sol_online

    else:
        
        worst_job = max([jobi for machine in sol_online for jobi in machine])
        if job>=2*worst_job and len(jobs)>5 or high_value == True:
            for i in range(m): 
                temp_solution = [lst[:] for lst in sol_online]
                temp_solution[i].append(job)
                score=simulate_makespan(temp_solution, fast_nb, slow_speed)
                if score < best_score:
                    best_score = score
                    best_solution = temp_solution
            for i in range(m):
                sol_online[i] = best_solution[i][:]  
            high_value=True
            return sol_online

        else:
            if len(jobs)<=3:               
                for _ in range(100):
                    alpha=random.random()
                    for k in range(fast_nb-1,m):
                        temp_solution = [lst[:] for lst in sol_online]
                        machine_index = k
                        temp_solution[machine_index].append(job)
                        for l in range(m):
                            machine_index_future = l
                            machine_future = [lst[:] for lst in temp_solution]
                                
                            machine_future[machine_index_future].append(2*worst_job)
                            
                            score_now=simulate_makespan(temp_solution, fast_nb, slow_speed)
                            score_future = simulate_makespan(machine_future, fast_nb, slow_speed)
                            
                            if alpha*score_now + (1-alpha)*score_future < best_score:
                                best_score = alpha*score_now + (1-alpha)*score_future
                                best_solution = temp_solution
            else:    
                for _ in range(100):
                    alpha=random.random()
                    for k in range(m):
                        temp_solution = [lst[:] for lst in sol_online]
                        machine_index = k
                        temp_solution[machine_index].append(job)
                        for l in range(m):
                            machine_index_future = l
                            machine_future = [lst[:] for lst in temp_solution]
                                
                            machine_future[machine_index_future].append(2*worst_job)
                            
                            score_now=simulate_makespan(temp_solution, fast_nb, slow_speed)
                            score_future = simulate_makespan(machine_future, fast_nb, slow_speed)
                            
                            if alpha*score_now + (1-alpha)*score_future < best_score:
                                best_score = alpha*score_now + (1-alpha)*score_future
                                best_solution = temp_solution

            for i in range(m):
                sol_online[i] = best_solution[i][:]
            
        return sol_online

def simulate_makespan(sol_online, fast_nb, slow_speed):
    return max([sum(machine) * (fast_speed if idx < fast_nb else slow_speed) for idx, machine in enumerate(sol_online)])

def select_machine_based_on_heuristic(sol_online, fast_nb, slow_speed):
    loads = [sum(machine) * (fast_speed if idx < fast_nb else slow_speed) for idx, machine in enumerate(sol_online)]
    if random.random() < 0.6:
        return loads.index(min(loads))
    else:
        return random.randint(0, len(loads) - 1)

##############################################################
#### LISEZ LE README et NE PAS MODIFIER LE CODE SUIVANT ####
##############################################################
if __name__=="__main__":

    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])
    
    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(output_dir, "doesn't exist")
        exit()       
	
    # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))             
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    # le bloc de lancement dégagé à l'exterieur pour ne pas le répeter pour deterministe/random
    def launching_sequence(sigma, m, fast_nb, slow_speed):
         ### global sol_online # car effacé en ingestion !!!
        sol_online  = [[] for i in range(m)]    
        for job in sigma:
            # votre algoritme est lancé ici pour une tâche job
            slow_fast_scheduling_online(sol_online, m, fast_nb, slow_speed, job)

        # Un algorithme doit attribuer toutes les tâches aux machines
        verify_solution(sigma, sol_online)
        return sol_online # retour nécessaire pour ingestion



    # Collecte des résultats
    scores = []
    
    for instance_filename in sorted(os.listdir(input_dir)):
        
        # C'est une partie pour inserer dans ingestion.py !!!!!
        # importer l'instance depuis le fichier (attention code non robuste)
        # le code repris de Safouan - refaire pour m'affanchir des numéros explicites
        instance_file = open(os.path.join(input_dir, instance_filename), "r")
        lines = instance_file.readlines()
        
        m = int(lines[1])
        fast_nb = int(lines[4])
        slow_nb = m-fast_nb
        slow_speed = int(lines[7])
        str_lu_sigma = lines[10]
        sigma = ast.literal_eval(str_lu_sigma)
        exact_solution = int(lines[13])

        # lancement conditionelle de votre algorithme
        # N.B. il est lancé par la fonction launching_sequence() 
        if mon_algo_est_deterministe():
            print("lancement d'un algo deterministe")  
            solution_online = launching_sequence(sigma, m, fast_nb, slow_speed)
            solution_eleve = val_sol(sigma, m, fast_nb, slow_speed, solution_online)  
        else:
            print("lancement d'un algo randomisé")
            runs = 10
            sample = numpy.empty(runs)
            for r in range(runs):
                solution_online = launching_sequence(sigma, m, fast_nb, slow_speed)  
                sample[r] = val_sol(sigma, m, fast_nb, slow_speed, solution_online)
            solution_eleve = numpy.mean(sample)


        best_ratio = solution_eleve/float(exact_solution)
        scores.append(best_ratio)
        # ajout au rapport
        output_file.write(instance_filename + ': score: {}\n'.format(best_ratio))

    output_file.write("Résultat moyen des ratios:" + str(sum(scores)/len(scores)))

    output_file.close()
