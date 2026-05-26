import random
import matplotlib.pyplot as plt

# Data barang

barang = [
    ("Barang1", 10, 5),
    ("Barang2", 40, 4),
    ("Barang3", 30, 6),
    ("Barang4", 50, 3),
    ("Barang5", 35, 7)
]

kapasitas_maksimal = 15

# 2 digit terakhir NIM

nim = 134
dua_digit_terakhir = nim % 100

# Inisialisasi populasi

def inisialisasi_populasi(
    jumlah_populasi,
    jumlah_gen
):

    populasi = []

    for i in range(jumlah_populasi):

        kromosom = [
            random.randint(0, 1)
            for _ in range(jumlah_gen)
        ]

        populasi.append(kromosom)

    return populasi

# Menghitung fitness

def hitung_fitness(kromosom):

    total_keuntungan = 0
    total_ukuran = 0

    for i in range(len(kromosom)):

        if kromosom[i] == 1:

            total_keuntungan += barang[i][1]
            total_ukuran += barang[i][2]

    if total_ukuran > kapasitas_maksimal:
        return 0

    return total_keuntungan

# Tournament Selection

def tournament_selection(
    populasi,
    fitness_populasi,
    k=3
):

    peserta_index = random.sample(
        range(len(populasi)),
        k
    )

    peserta = []

    for i in peserta_index:

        peserta.append(
            (populasi[i], fitness_populasi[i])
        )

    peserta.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return peserta[0][0]

# Two Point Crossover

def two_point_crossover(
    parent1,
    parent2
):

    titik1 = random.randint(
        1,
        len(parent1)-2
    )

    titik2 = random.randint(
        titik1+1,
        len(parent1)-1
    )

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

    posisi1 = random.randint(
        0,
        len(kromosom)-2
    )

    posisi2 = random.randint(
        posisi1+1,
        len(kromosom)-1
    )

    kromosom[posisi1:posisi2] = list(
        reversed(
            kromosom[posisi1:posisi2]
        )
    )

    return kromosom

# Main Program

def run_ga():

    jumlah_generasi = dua_digit_terakhir
    jumlah_populasi = 20
    jumlah_gen = len(barang)

    prob_mutasi = dua_digit_terakhir / 100
    prob_crossover = 0.8

    populasi = inisialisasi_populasi(
        jumlah_populasi,
        jumlah_gen
    )

    best_fitness_list = []
    worst_fitness_list = []
    avg_fitness_list = []
    all_fitness = []

    best_solution = None
    best_fitness = 0

    # Proses generasi

    for generasi in range(jumlah_generasi):

        fitness_populasi = [

            hitung_fitness(individu)

            for individu in populasi
        ]

        fitness_terbaik = max(
            fitness_populasi
        )

        fitness_terendah = min(
            fitness_populasi
        )

        fitness_rata = (
            sum(fitness_populasi)
            / len(fitness_populasi)
        )

        best_fitness_list.append(
            fitness_terbaik
        )

        worst_fitness_list.append(
            fitness_terendah
        )

        avg_fitness_list.append(
            fitness_rata
        )

        all_fitness.append(
            fitness_populasi.copy()
        )

        index_best = fitness_populasi.index(
            fitness_terbaik
        )

        if fitness_terbaik > best_fitness:

            best_fitness = fitness_terbaik

            best_solution = populasi[index_best]

        print(f"\nGenerasi {generasi+1}")

        print(
            "Fitness Terbaik:",
            fitness_terbaik
        )

        # Populasi baru

        new_populasi = []

        while len(new_populasi) < jumlah_populasi:

            parent1 = tournament_selection(
                populasi,
                fitness_populasi
            )

            parent2 = tournament_selection(
                populasi,
                fitness_populasi
            )

            # Crossover

            if random.random() < prob_crossover:

                anak1, anak2 = two_point_crossover(
                    parent1,
                    parent2
                )

            else:

                anak1 = parent1[:]
                anak2 = parent2[:]

            # Mutasi

            if random.random() < prob_mutasi:

                anak1 = inversion_mutation(
                    anak1
                )

            if random.random() < prob_mutasi:

                anak2 = inversion_mutation(
                    anak2
                )

            new_populasi.extend(
                [anak1, anak2]
            )

        populasi = new_populasi[
            :jumlah_populasi
        ]

    # Hasil terbaik

    print("\n===== HASIL TERBAIK =====")

    print(
        "Kromosom :",
        best_solution
    )

    print(
        "Fitness :",
        best_fitness
    )

    print("\nBarang Terpilih:")

    total_ukuran = 0

    for i in range(len(best_solution)):

        if best_solution[i] == 1:

            print(barang[i][0])

            total_ukuran += barang[i][2]

    print(
        "Total Ukuran:",
        total_ukuran
    )

    # Grafik fitness

    plt.figure(figsize=(12,7))

    for i in range(jumlah_generasi):

        x = [i+1] * len(all_fitness[i])

        y = all_fitness[i]

        plt.scatter(
            x,
            y,
            color='gray',
            alpha=0.2
        )

    plt.plot(
        range(1, jumlah_generasi+1),
        best_fitness_list,
        color='blue',
        label='Fitness Tertinggi'
    )

    plt.plot(
        range(1, jumlah_generasi+1),
        avg_fitness_list,
        color='red',
        label='Fitness Rata-rata'
    )

    plt.plot(
        range(1, jumlah_generasi+1),
        worst_fitness_list,
        color='yellow',
        label='Fitness Terendah'
    )

    plt.title(
        'Perkembangan Nilai Fitness\n'
        'Seleksi: Tournament | '
        'Crossover: Two Point | '
        'Mutasi: Inversion'
    )

    plt.xlabel('Generasi')

    plt.ylabel(
        'Nilai Fitness (Keuntungan)'
    )

    plt.legend()

    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    run_ga()
