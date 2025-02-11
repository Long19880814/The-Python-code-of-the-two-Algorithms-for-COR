import numpy as np
import pandas as pd

def algorithm_mixed_h(M, h, J, p_j, s_i):
    sorted_jobs = sorted(J, key=lambda j: p_j[j])
    S_machines = M[:h]
    L_machines = M[h:]
    M_jobs = {i: [] for i in M}
    l = 0
    t = len(sorted_jobs)

    while l != t:
        machine_ratios = {i: (p_j[sorted_jobs[t - 1]] + sum(p_j[j] for j in M_jobs[i])) / s_i[i] for i in M}
        i_1 = min(M, key=lambda i: machine_ratios[i])

        if i_1 > h:
            M_jobs[i_1].append(sorted_jobs[t - 1])
            t -= 1
        else:
            l += 1
            S_machine_ratios = {i: (p_j[sorted_jobs[l - 1]] + sum(p_j[j] for j in M_jobs[i])) / s_i[i] for i in S_machines}
            i_2 = min(S_machines, key=lambda i: S_machine_ratios[i])
            M_jobs[i_2].append(sorted_jobs[l - 1])

    for machine in L_machines:
        remaining_jobs = sorted(M_jobs[machine], key=lambda j: p_j[j], reverse=True)
        M_jobs[machine] = remaining_jobs

    return M_jobs

def opt_schedule_tasks(J, p_j, M, s_i):
    n = len(J)
    m = len(M)
    fractions = []
    for machine in M:
        for j in range(1, n + 1):
            fractions.append((j / s_i[machine], machine, j))
    fractions = sorted(fractions)[:n]
    sorted_jobs = sorted(J, key=lambda x: p_j[x], reverse=True)
    schedule = [[] for _ in range(m)]
    for job, (value, machine, position) in zip(sorted_jobs, fractions):
        schedule[M.index(machine)].append((position, job))

    for i in range(m):
        schedule[i].sort(reverse=True)
    opt_job_completion_times = {}
    for i in range(m):
        opt_job_current_time = 0
        for position, job in schedule[i]:
            opt_job_current_time += p_j[job] / s_i[M[i]]
            opt_job_completion_times[job] = opt_job_current_time

    opt_total_completion_time = sum(opt_job_completion_times.values())
    return opt_total_completion_time

def run_schedule_algorithm(J):
    M = [1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16]
    h = 13
    p_j = {j: np.random.randint(1, 101) for j in J}
    random_values = [np.random.randint(1, 21) for _ in M]
    sorted_values = sorted(random_values)
    s_i = {i: sorted_values[idx] for idx, i in enumerate(M)}

    print("processing time：", p_j)
    print("machine speed：", s_i)

    total_processing_time = sum(p_j.values())
    max_processing_time = max(p_j.values())
    total_speed = sum(s_i.values())
    max_speed = max(s_i.values())

    makespan = max(total_processing_time / total_speed, max_processing_time/ max_speed)
    lb = opt_schedule_tasks(J, p_j, M, s_i)
    schedule = algorithm_mixed_h(M, h, J, p_j, s_i)

    machine_completion_times = {machine: sum(p_j[j] for j in J) for machine, J in schedule.items()}
    max_completion_time = max(machine_completion_times.values())

    job_completion_times = {}
    for machine, J in schedule.items():
        current_time = 0
        for j in J:
            current_time += p_j[j]
            job_completion_times[j] = current_time

    total_completion_time = sum(job_completion_times.values())

    PoA_C = max_completion_time / makespan
    print("PoA_C : {:.4f}".format(PoA_C))
    PoA_T = total_completion_time / lb
    print("PoA_T : {:.4f}".format(PoA_T))

    return PoA_C, PoA_T

results = []

for J_value in range(20, 201, 20):
    print(f"\n----- J = {J_value} -----")
    PoA_C_values = []
    PoA_T_values = []
    for k in range(100):
        print(f"run {k+1} :")
        J = [j for j in range(1, J_value + 1)]
        PoA_C, PoA_T = run_schedule_algorithm(J)
        PoA_C_values.append(PoA_C)
        PoA_T_values.append(PoA_T)
        print("-" * 40)

    average_PoA_C = sum(PoA_C_values) / len(PoA_C_values)
    print(f"average_PoA_C (J={J_value}): {average_PoA_C:.4f}")

    average_PoA_T = sum(PoA_T_values) / len(PoA_T_values)
    print(f"average_PoA_T (J={J_value}): {average_PoA_T:.4f}")
    results.append((J_value, round(average_PoA_C, 4), round(average_PoA_T, 4)))

df = pd.DataFrame(results, columns=["J_value", "average_PoA_C", "average_PoA_T"]).transpose()
print(df.to_string(header=True))

