import numpy as np
import pandas as pd
import heapq

def modified_algorithm_mixed_h(M, h, SPT, LPT, J, p_j):
    sorted_jobs = sorted(J, key=lambda j: p_j[j])
    S_machines = list(range(1, h + 1))
    L_machines = list(range(h + 1, len(M) + 1))
    S_jobs = sorted_jobs[:h]
    remaining_jobs = sorted_jobs[h:]
    M_jobs = {i: [] for i in M}

    for i in range(h):
        M_jobs[S_machines[i]].append(S_jobs[i])
    L_jobs = remaining_jobs[-(len(M) - h):]
    remaining_jobs = remaining_jobs[:-(len(M) - h)]

    for i in range(len(M) - h):
        M_jobs[L_machines[i]].append(L_jobs[i])
    l = h + 1
    t = len(sorted_jobs) - (len(M) - h)

    while l <= t:
        S_machines_processing_time = {i: sum(p_j[j] for j in M_jobs[i]) for i in S_machines}
        L_machines_processing_time = {i: sum(p_j[j] for j in M_jobs[i]) for i in L_machines}
        i_1 = min(S_machines, key=lambda i: S_machines_processing_time[i])
        i_2 = min(L_machines, key=lambda i: L_machines_processing_time[i])
        if (S_machines_processing_time[i_1] + p_j[sorted_jobs[l - 1]] <= L_machines_processing_time[i_2] + p_j[sorted_jobs[t - 1]]):
            M_jobs[i_1].append(sorted_jobs[l - 1])
            l += 1
        else:
            M_jobs[i_2].append(sorted_jobs[t - 1])
            t -= 1

    return M_jobs

def spt_schedule(M, J, p_j):

    sorted_jobs = sorted(p_j.items(), key=lambda item: item[1])
    machines = [0] * len(M)
    heapq.heapify(machines)
    spt_job_completion_times = {j: 0 for j in J}

    index = 0
    while index < len(J):
        for i in range(min(len(M), len(J) - index)):
            spt_earliest_finish_time = heapq.heappop(machines)
            job_id, job_time = sorted_jobs[index]
            new_finish_time = spt_earliest_finish_time + job_time
            heapq.heappush(machines, new_finish_time)
            spt_job_completion_times[job_id] = new_finish_time
            index += 1

    return sum(spt_job_completion_times.values())

def run_schedule_algorithm(J):
    M = [1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16]
    h = 13
    SPT = True
    LPT = True
    p_j = {j: np.random.randint(1, 101) for j in J}

    print("processing time：", p_j)

    total_processing_time = sum(p_j.values())
    max_processing_time = max(p_j.values())
    makespan = max(total_processing_time / len(M), max_processing_time)
    lb = spt_schedule(M, J, p_j)
    print(f"the lb of makespan：{makespan}")
    print(f"the lb of total completion time：{lb}")

    schedule = modified_algorithm_mixed_h(M, h, SPT, LPT, J, p_j)

    print(schedule)

    machine_completion_times = {machine: sum(p_j[j] for j in J) for machine, J in schedule.items()}

    for machine, completion_time in machine_completion_times.items():
        print(f"completion time of {machine}：{completion_time}")
    max_completion_time = max(machine_completion_times.values())
    print(f"max completion time：{max_completion_time}")
    job_completion_times = {}

    for machine, J in schedule.items():
        current_time = 0
        for j in J:
            current_time += p_j[j]
            job_completion_times[j] = current_time

    for j, completion_time in job_completion_times.items():
        print(f"completion time of job {j}：{completion_time}")
    total_completion_time = sum(job_completion_times.values())
    print(f"total completion time：{total_completion_time}")

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

