import pickle
green_time = pickle.load(open('./green.pkl', 'rb'))



def evaluate(t1, t2, t3, t4, lane_density ):
    global green_time

    res = [0,0]
    static_traffic = [t1, t2, t3, t4]
    dynamic_traffic = [t1, t2, t3, t4]

    def_green_time = 17.5
    def_traffic_output = 2.5
    ped_crossing = 12

    while sum(static_traffic)>0:
        for i in range(4):
            cur_green_time = def_green_time
            static_traffic[i] = max(0, static_traffic[i]- def_traffic_output*cur_green_time)
            res[0]+=cur_green_time
            if sum(static_traffic)<=0:
                break
        res[0] += ped_crossing
    lane_green_time = [0, 0, 0, 0]

    for i in range(4):
        green_time.input['current'] = lane_density[i]
        green_time.input['others'] = (sum(lane_density)-lane_density[i])/3
        green_time.compute()
        lane_green_time[i] = green_time.output['green']

    while sum(dynamic_traffic)>0:
        for i in range(4):
            cur_green_time = lane_green_time[i]
            dynamic_traffic[i] = max(0, dynamic_traffic[i]- def_traffic_output*cur_green_time)
            res[1]+=cur_green_time
            if sum(dynamic_traffic)<=0:
                break
        res[1] += ped_crossing
    
    return res

lane_densities = [
    [ 15, 9, 12, 15 ],
    [ 15, 36, 53, 42 ],
    [ 15, 77, 78, 87 ],
    [ 50, 11, 13, 29 ],
    [ 50, 49, 55, 54 ],
    [ 50, 79, 75, 80 ],
    [ 85, 10, 19, 25 ],
    [ 85, 39, 49, 52 ],
    [ 85, 89, 75, 80 ],
    [ 13, 14, 53, 48 ],
    [ 14, 16, 80, 79 ],
    [ 53, 51, 83, 79 ]
]

print()
for i in lane_densities:
    j = [k for k in i]
    res = evaluate(*j, i) 
    print(res[0] , "\t", round(res[1],2))
    print( round(res[0]-res[1] , 4))
    print( round((res[0]-res[1])/res[0]*100 , 2 ))