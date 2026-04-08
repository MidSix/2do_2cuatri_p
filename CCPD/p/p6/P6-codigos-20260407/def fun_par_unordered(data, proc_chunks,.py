def fun_par_unordered(data, proc_chunks, resultsPar):
    with ProcessPoolExecutor(max_workers=N_PROC) as executor:
        total_runtime = 0
        start = time.time()
        futures = list()
        for ini, end in proc_chunks:
            for fun in FUNCS:
                futures.append((fun.__name__, executor.submit(fun, data[ini:end])))

        for fun_name, f in futures:
            result, runtime = f.result()
            resultsPar[fun_name].append(result)
            total_runtime += runtime
        end = time.time()
        time_granted = N_PROC * to_time_miliseconds(start, end)
        time_efficiency = "{0} %".format(int(100 * (total_runtime / time_granted)))
    return resultsPar, time_efficiency