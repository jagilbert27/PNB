import pandas
print('howdy')

imported = pandas.read_csv('student_import.csv').transpose()

for label, content in imported.items():
    print(f'label: {label}')
    print(f'content: {content}', sep='\n')
    for item in content:
        print(item)


# print(imported)

# print(imported.items()[2])


# for row in imported:
#     print(row)

