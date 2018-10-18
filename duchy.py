from random import randint
print("Gra w duchy")
mam_odwage=True
wynik=0
while mam_odwage:
    drzwi_ducha=randint(1,3)
    #print(drzwi_ducha)
    print("Przed Toba troje drzwi...")
    print("Za jednymi jest duch.")
    print("Ktore otwierasz?")
    drzwi=input("1, 2 czy 3? ")
    drzwi=int(drzwi)
    if drzwi==drzwi_ducha:
        print('DUUUUCH!')
        mam_odwage=False
    else:
        print('Nie ma ducha :)')
        print('Wchodzisz do nastepnego pokoju.')
        wynik=wynik+1
print('Uciekaj!')
print('Koniec gry! Twoj wynik: ', wynik)
              
