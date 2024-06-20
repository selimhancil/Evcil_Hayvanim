from datetime import datetime, timedelta

class Pet:
    MAX_HEALTH = 5  # Hayvanın sağlık puanı

    def __init__(self, name):
        self.name = name
        self.tokluk = 100  # Tokluk 0-100 arası, başlangıç 100
        self.happiness = 50  # Mutluluk 0-100 arası, başlangıç 50
        self.health = self.MAX_HEALTH  # Sağlık puanı
        self.is_sick = False
        self.last_interaction = datetime.now()

    def feed(self):
        if self.is_sick:
            print(f"{self.name} hastalandı Şu anda yemek yiyemez durumda")
            return
        
        self.tokluk += 10
        if self.tokluk > 100:
            self.tokluk = 100
        
        print(f"{self.name} beslendi Tokluk durumu: {self.tokluk}")
        self.status()
    
    def play(self):
        self.tokluk -= 5  # Oyun oynadığında tokluğu 5 azalt
        if self.tokluk < 0:
            self.tokluk = 0
        
        self.happiness += 10  # Oyun oynandığında mutluluğu 10 arttır
        if self.happiness > 100:
            self.happiness = 100
        
        print(f"{self.name} ile oynandı Mutluluk durumu: {self.happiness}, Tokluk durumu: {self.tokluk}")
        self.status()
    
    def status(self):
        status = f"{self.name} - Tokluk: {self.tokluk}, Mutluluk: {self.happiness}, Sağlık: {self.health}/{self.MAX_HEALTH}"
        if self.is_sick:
            status += ", Durum: Hasta"
        print(status)
    
    def pass_time(self, time_difference_in_minutes=None):
        current_time = datetime.now()
        if time_difference_in_minutes is None:
            time_since_last_interaction = current_time - self.last_interaction
            time_difference_in_minutes = time_since_last_interaction.total_seconds() / 60
        
        self.tokluk -= 5 * time_difference_in_minutes
        if self.tokluk < 0:
            self.tokluk = 0
        
        self.happiness -= 5 * time_difference_in_minutes
        if self.happiness < 0:
            self.happiness = 0
        
        if self.tokluk <= 20 or self.happiness <= 20:
            self.is_sick = True
            if self.tokluk <= 20:
                print(f"{self.name} yemek vermediğin için hastalandı")
            if self.happiness <= 20:
                print(f"{self.name} oynamadığın için hastalandı")
            self.health -= 1
            self.tokluk = 100  # Hasta olduğunda tokluk 100 olsun
            if self.health <= 0:
                print(f"{self.name} ÖLDÜ!")
                return False
        
        if self.health < self.MAX_HEALTH and not self.is_sick:
            self.health += 1
        
        self.last_interaction = current_time
        return True

class User:
    MAX_PETS = 3

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.pets = []
        self.last_interaction = datetime.now()
        self.banned_until = None

    def add_pet(self, pet):
        if len(self.pets) < self.MAX_PETS:
            self.pets.append(pet)
            print(f"{pet.name} adında yeni bir evcil hayvan ekledinn. Hadi hayırlı olsun")
        else:
            print("Kaç hayvana bakıcan abi, biraz sabır!")

    def update_interaction_time(self):
        self.last_interaction = datetime.now()

    def pass_time(self):
        current_time = datetime.now()
        time_since_last_interaction = current_time - self.last_interaction
        time_difference_in_minutes = time_since_last_interaction.total_seconds() / 60

        for pet in self.pets:
            alive = pet.pass_time(time_difference_in_minutes)
            if not alive:
                self.pets.remove(pet)
                self.ban_user()
                break

    def ban_user(self):
        self.banned_until = datetime.now() + timedelta(weeks=1)
        print(f"Kullanıcı {self.username}, evcil hayvanının ölmesi nedeniyle 1 hafta süreyle banlandı.")
        exit()  # Banlandığında oyundan çıkış yaptırır

def register(users):
    username = input("Kullanıcı adınızı girin: ")
    if username in users:
        print("Bu kullanıcı adı zaten alınmış lütfen başka bir kullanıcı adı seç")
        return None
    
    password = input("Şifrenizi girin: ")
    users[username] = User(username, password)
    print(f"{username} başarıyla kaydoldun")
    return users[username]

def login(users):
    username = input("Kullanıcı adınızı girin: ")
    if username not in users:
        print("Bu kullanıcı adı bulunamadı,lütfen hemen kaydol")
        return None
    
    password = input("Şifrenizi girin: ")
    if users[username].password != password:
        print("Yanlış şifre tekrar dene")
        return None
    
    if users[username].banned_until and datetime.now() < users[username].banned_until:
        print(f"Kullanıcı {username}, {users[username].banned_until} tarihine kadar banlanmıştır")
        return None
    
    print(f"Hoş geldiniz, {username}!")
    return users[username]

def main():
    users = {}
    current_user = None
    
    while True:
        print("\n1. Giriş yap")
        print("2. Kaydol")
        print("3. Çıkış")
        
        choice = input("Seçiminiz: ")
        
        if choice == "1":
            current_user = login(users)
            if current_user:
                break
        elif choice == "2":
            current_user = register(users)
            if current_user:
                break
        elif choice == "3":
            print("Güle güle!")
            return
        else:
            print("Geçersiz seçim tekrar denee")
    
    if current_user.pets == []:
        pet_name = input("Evcil hayvanınızın adını girin: ")
        current_user.add_pet(Pet(pet_name))
    
    while True:
        print("\nNe yapmak istersi?")
        print("1. Evcil hayvanı besle")
        print("2. Evcil hayvan ile oyna")
        print("3. Evcil hayvanların durumunu kontrol et")
        print("4. Çıkış")
        
        choice = input("Seçiminiz: ")
        
        if choice == "1":
            for pet in current_user.pets:
                pet.feed()
                pet.pass_time()
                if pet.health <= 0:
                    current_user.ban_user()
                    break
        elif choice == "2":
            for pet in current_user.pets:
                pet.play()
                pet.pass_time()
                if pet.health <= 0:
                    current_user.ban_user()
                    break
        elif choice == "3":
            for pet in current_user.pets:
                pet.status()
        elif choice == "4":
            print("Oyun bitti. HOŞÇAKALL!")
            break
        else:
            print("Geçersiz seçim, Tekrar dene")

if __name__ == "__main__":
    main()
