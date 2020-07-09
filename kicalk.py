import yaml
import os.path
from pprint import pprint
import lib_kicalk

#config_file = "~/_curent/skap/total_calk.yaml"
config_file = "settings.yaml"
projects=list()
report=list()

def main():
    print(config_file)
    with open(config_file) as f:
        conf=yaml.load(f, yaml.FullLoader)
    # pprint(conf)
    # pprint(conf['Settings'])
    # print(project_names)
    projects=conf['projects']
    # pprint(projects)
    for proj in projects:
        name=[*proj][0]
        path:str=proj[name][0]['path']
        path = path.replace('~',os.path.expanduser('~'))
        company=proj[name][0]['company']
        pay_per_hour=proj[name][0]['pay_per_hour']
        if os.path.isfile(path):
            time_tobill=lib_kicalk.calc_proj(path)[2]
            # report.append([name,company,time_tobill,pay_per_hour])
            report.append({"name":name,"company":company,"time_tobill":time_tobill,"pay_per_hour":pay_per_hour})
            # print(f'For the project {name} bill {company} for {time_tobill}')
        else:
            print(f'File\n{path}\nDoes not exists')
            report.append({"name":name,"company":company,"time_tobill":"ERROR: pah","pay_per_hour":0})

    print("=========[ Summary ]===========\n\n")
    for r in report:
        print(f'===[ {r["company"]}]===')
        print(f'Bill {r["company"]} for the project {r["name"]}')
        print(f'The bill is for {r["time_tobill"][0]}hours and {r["time_tobill"][1]}minutes at the rate of {r["pay_per_hour"]}kr/hr')
        billing=(r["time_tobill"][0] + r["time_tobill"][1]/60)*r["pay_per_hour"]
        print(f'Thus bill for {billing:.2f}kr')
        print("\n")

if __name__ == '__main__':
    main()
