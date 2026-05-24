import random
import matplotlib.pyplot as plt

barang = [
    ("Barang1", 10, 5),
    ("Barang2", 40, 4),
    ("Barang3", 30, 6),
    ("Barang4", 50, 3),
    ("Barang5", 35, 7)
]

kapasitas_gudang = 15

jumlah_generasi = 50
jumlah_populasi = 20
prob_crossover = 0.8
prob_mutasi = 0.1

best_fitness_list = []

# Inisialisasi populasi
def inisialisasi_populasi():
    return [
        [random.randint(0, 1) for _ in range(len(barang))]
        for _ in range(jumlah_populasi)
    ]

# Menghitung fitness
def hitung_fitness(kromosom):

    total_keuntungan = 0
    total_ukuran = 0

    for i in range(len(kromosom)):

        if kromosom[i] == 1:
            total_keuntungan += barang[i][1]
            total_ukuran += barang[i][2]

    if total_ukuran > kapasitas_gudang:
        return 0

    return total_keuntungan

# Tournament Selection
def tournament_selection(populasi):

    peserta = random.sample(populasi, 3)

    return max(
        peserta,
        key=hitung_fitness
    )

# Two Point Crossover
def two_point_crossover(parent1, parent2):

    titik1 = random.randint(1, len(parent1)-2)
    titik2 = random.randint(titik1+1, len(parent1)-1)

    anak1 = (
        parent1[:titik1]
        + parent2[titik1:titik2]
        + parent1[titik2:]
    )

    anak2 = (
        parent2[:titik1]
        + parent1[titik1:titik2]
        + parent2[titik2:]
    )

    return anak1, anak2

# Inversion Mutation
def inversion_mutation(kromosom):

    posisi1 = random.randint(0, len(kromosom)-2)
    posisi2 = random.randint(posisi1+1, len(kromosom)-1)

    kromosom[posisi1:posisi2] = list(
        reversed(kromosom[posisi1:posisi2])
    )

    return kromosom

# Populasi awal
populasi = inisialisasi_populasi()

best_individu = None
best_fitness = 0

# Proses algoritma genetika
for generasi in range(jumlah_generasi):

    fitness_populasi = [
        hitung_fitness(individu)
        for individu in populasi
    ]

    best_generasi = max(fitness_populasi)

    best_fitness_list.append(
        best_generasi
    )

    if best_generasi > best_fitness:

        best_fitness = best_generasi

        idx = fitness_populasi.index(
            best_generasi
        )

        best_individu = populasi[idx]

    new_populasi = []

    while len(new_populasi) < jumlah_populasi:

        parent1 = tournament_selection(
            populasi
        )

        parent2 = tournament_selection(
            populasi
        )

        if random.random() < prob_crossover:

            anak1, anak2 = two_point_crossover(
                parent1,
                parent2
            )

        else:

            anak1 = parent1[:]
            anak2 = parent2[:]

        if random.random() < prob_mutasi:
            anak1 = inversion_mutation(anak1)

        if random.random() < prob_mutasi:
            anak2 = inversion_mutation(anak2)

        new_populasi.extend([
            anak1,
            anak2
        ])

    populasi = new_populasi[:jumlah_populasi]

# Menampilkan hasil
print("\n=== HASIL TERBAIK ===")

print(
    "Kromosom Terbaik:",
    best_individu
)

print(
    "Keuntungan Maksimum:",
    best_fitness
)

print("\nBarang yang Dipilih:")

total_ukuran = 0

for i in range(len(best_individu)):

    if best_individu[i] == 1:

        print(
            f"{barang[i][0]}"
            f" | Keuntungan={barang[i][1]}"
            f" | Ukuran={barang[i][2]}"
        )

        total_ukuran += barang[i][2]

print(
    "\nTotal Ukuran:",
    total_ukuran
)

# Grafik fitness
plt.plot(best_fitness_list)
plt.title("Perkembangan Fitness")
plt.xlabel("Generasi")
plt.ylabel("Fitness")
plt.grid(True)
plt.show()