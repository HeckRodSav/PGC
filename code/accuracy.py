#!/usr/bin/python3

import sys

is_raw = ''

print(sys.argv, len(sys.argv))

if (len(sys.argv) >= 2) and (sys.argv[1] == "raw"):
	from image_list_raw import img_array_names
	is_raw = '_raw'
else:
	from image_list import img_array_names

total = len(img_array_names)

types = {f"{i:0>4b}":0 for i in range(16) }
general = {f"{i:0>4b}":0 for i in range(16) }

for img in img_array_names:
	types[f"{img[1]:0>4b}"] += 1
	if img[1] == 0b0000 :
		general["0000"] += 1
	else:
		general[f"{img[1]&0b1100:0>4b}"] += 1
		general[f"{img[1]&0b0011:0>4b}"] += 1

total_read = total
total_read -= types['0101']
total_read -= types['1101']
total_read -= types['1001']

ordem = [1,3,2]
colunas = {1: 'Não encontrado', 3: 'Semelhante', 2: 'Encontrado'}
linhas = {1: 'Leitura incorreta', 3: 'Leitura parcial', 2: 'Leitura correta'}
totais = {1:['',''], 2:['\\textbf{','}'], 3:['\\textbf{','}']}
if is_raw != '':
	totais = {1: ['',''], 2:['',''], 3:['','']}

print()

print(end='\t')
for j in ordem:
	j_aux = f'{j:0>2b}'
	print(f'{j_aux:X<4}', end='\t')
print("Total")
for i in ordem:
	i_aux = f'{i:0>2b}'
	print(f'{i_aux:X>4}', end='\t')
	for j in ordem:
		j_aux = f'{j:0>2b}'
		print(types[j_aux+i_aux], end='\t')
		# print(j_aux+i_aux, end='\t')
	print(general['00'+i_aux])
print('Total',end='\t')
for j in ordem:
	j_aux = f'{j:0>2b}'
	print(general[j_aux+'00'],end='\t')
print(total)

print()

print(end='\t')
for j in ordem:
	j_aux = f'{j:0>2b}'
	print(f'{j_aux:X<4}', end='\t')
print("Total")
for i in ordem:
	i_aux = f'{i:0>2b}'
	print(f'{i_aux:X>4}', end='\t')
	for j in ordem:
		j_aux = f'{j:0>2b}'
		print(f"{(types[j_aux+i_aux]/total*100):0>5.1f}%", end='\t')
	print(f"{(general['00'+i_aux]/total*100):0>5.1f}%")
print('Total',end='\t')
for j in ordem:
	j_aux = f'{j:0>2b}'
	print(f"{(general[j_aux+'00']/total*100):0>5.1f}%",end='\t')
print(f"{(total/total*100):0>5.1f}%")

print()

log_geral = open(f'geral{is_raw}.dat', 'w')

print(f'{total} itens', sep='', end='\t', file = log_geral)
for j in ordem:
	print(colunas[j], end='\t', file = log_geral)
print("Total", file = log_geral)
for i in ordem:
	i_aux = f'{i:0>2b}'
	print('\\textbf{', linhas[i], '}', sep='', end='\t', file = log_geral)
	for j in ordem:
		j_aux = f'{j:0>2b}'
		print("\SI{",f"{(types[j_aux+i_aux]/total*100):0>5.1f}","}{\percent}", end='\t', sep='', file = log_geral)
	print(totais[i][0],"\SI{",f"{(general['00'+i_aux]/total*100):0>5.1f}","}{\percent}", totais[i][1], sep='', file = log_geral)
print('\\textbf{Total}',end='\t', file = log_geral)
for j in ordem:
	j_aux = f'{j:0>2b}'
	print("\SI{",f"{(general[j_aux+'00']/total*100):0>5.1f}","}{\percent}", end='\t', sep='', file = log_geral)
print("\SI{",f"{(total/total*100):0>5.1f}","}{\percent}", sep='', file = log_geral)

log_geral.flush()
log_geral.close()


print()
print('-'*40)
print()


for i in ordem:
	i_aux = f'{i:0>2b}'
	general[i_aux+'00'] -= types[i_aux+'01']

print(end='\t')
for j in ordem:
	j_aux = f'{j:0>2b}'
	print(f'{j_aux:X<4}', end='\t')
print("Total")
for i in ordem[1:]:
	i_aux = f'{i:0>2b}'
	print(f'{i_aux:X>4}', end='\t')
	for j in ordem:
		j_aux = f'{j:0>2b}'
		print(types[j_aux+i_aux], end='\t')
	print(general['00'+i_aux])
print('Total',end='\t')
for j in ordem:
	j_aux = f'{j:0>2b}'
	print(general[j_aux+'00'],end='\t')
print(total_read)

print()

print(end='\t')
for j in ordem:
	j_aux = f'{j:0>2b}'
	print(f'{j_aux:X<4}', end='\t')
print("Total")
for i in ordem[1:]:
	i_aux = f'{i:0>2b}'
	print(f'{i_aux:X>4}', end='\t')
	for j in ordem:
		j_aux = f'{j:0>2b}'
		print(f"{(types[j_aux+i_aux]/total_read*100):0>5.1f}%", end='\t')
	print(f"{(general['00'+i_aux]/total_read*100):0>5.1f}%")
print('Total',end='\t')
for j in ordem:
	j_aux = f'{j:0>2b}'
	print(f"{(general[j_aux+'00']/total_read*100):0>5.1f}%",end='\t')
print(f"{(total_read/total_read*100):0>5.1f}%")

print()


log_lido = open(f'lido{is_raw}.dat', 'w')

print(f'{total_read} itens', sep='', end='\t', file = log_lido)
for j in ordem:
	print(colunas[j], end='\t', file = log_lido)
print("Total", file = log_lido)
for i in ordem[1:]:
	i_aux = f'{i:0>2b}'
	print('\\textbf{', linhas[i], '}', sep='', end='\t', file = log_lido)
	for j in ordem:
		j_aux = f'{j:0>2b}'
		# print(j_aux+i_aux, end='\t')
		print("\SI{",f"{(types[j_aux+i_aux]/total_read*100):0>5.1f}", "}{\percent}", end='\t', sep='', file = log_lido)
	print("\SI{",f"{(general['00'+i_aux]/total_read*100):0>5.1f}", "}{\percent}", sep='', file = log_lido)
print('\\textbf{Total}',end='\t', file = log_lido)
for j in ordem:
	j_aux = f'{j:0>2b}'
	print(totais[j][0],"\SI{",f"{(general[j_aux+'00']/total_read*100):0>5.1f}", "}{\percent}",totais[j][1],end='\t', sep='', file = log_lido)
print("\SI{",f"{(total_read/total_read*100):0>5.1f}", "}{\percent}", sep='', file = log_lido)


log_lido.flush()
log_lido.close()
