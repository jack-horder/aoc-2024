import copy


def parse_report(file_name:str) -> list[list[int]]:
    reports:list[list[int]] = []
    with open(file=file_name, mode="r") as f:
        lines = f.readlines()
        for line in lines:
            reports.append(list(map(lambda x: int(x), line.split(sep=" "))))
    return reports

def report_check(report:list[int]) -> bool:
    ascending = False
    for i in range(len(report)-1):
        diff = report[i+1] - report[i]
        if abs(diff) > 3 or diff == 0:
            return False
        if i == 0:
            ascending = (diff < 0)
            continue
        if ascending != (diff < 0):
            return False
    return True

def day_2_part_1():
    reports = parse_report("day_2/puzzle_input.txt")
    safe_reports_count = 0
    for r in reports:
        if report_check(r):
            print(r)
            safe_reports_count +=1
    print("Safe Reports Count:")
    print(safe_reports_count)

def day_2_part_2():
    reports = parse_report("day_2/puzzle_input.txt")
    safe_reports_count = 0
    for r in reports:
        if report_check(r):
            print(r)
            safe_reports_count +=1
            continue
        for c in range(len(r)):
            r_copy = copy.copy(r)
            del r_copy[c]
            if report_check(r_copy):
                print(r_copy)
                safe_reports_count +=1
                break

    print("Safe Reports Count:")
    print(safe_reports_count)

def main():
    day_2_part_2()


if __name__ == "__main__":
    main()
