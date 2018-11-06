print("========================================")
print("===============KALKULATOR===============")
print("========================================")

sOpcja=1
while True:
    print("\r\nWybierz co chcesz zrobic:")
    print("1 - dodawanie")
    print("2 - odejmowanie")
    print("3 - mnozenie")
    print("4 - dzielenie")
    print("0 - koniec")
    sOpcja=input("")
    print(sOpcja, " ", type(sOpcja))
    if sOpcja=='0':
        break
    if sOpcja=='1':
        try:
            liczba1=float(input("Podaj skladnik 1: "))
            liczba2=float(input("Podaj skladnik 2: "))
            print("Wynik = ", liczba1+liczba2)
        except ValueError:
            print("5Bledna wartosc! Sprobuj jeszcze raz :)")
    elif sOpcja=='4':
        try:
            liczba1=float(input("Podaj dzielna: "))
            liczba2=float(input("Podaj dzielnik: "))
            if liczba2==0:
                print("Pamietaj cholero, nie dzielimy przez 0")
            else:
                print("\r\nWynik = ", liczba1/liczba2)
        except ValueError:
            print("Bledna wartosc! Sprobuj jeszcze raz :)")
    else:
        print("Bledny parametr!2")
            

