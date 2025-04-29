import re
fhand = open('/Users/wanakahideyuki/Desktop/regex_sum_2213414.txt')
sumation = 0
for line in fhand:
    line = line.rstrip()
    if re.findall('[0-9]+', line):
        numlist = re.findall('[0-9]+', line)
        for num in numlist:
            sumation = sumation + int(num)
print(sumation)
