import os
import stat
import win32security


def get_owner_info(file_path):
    sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
    owner_sid = sd.GetSecurityDescriptorOwner()
    name, domain, _ = win32security.LookupAccountSid(None, owner_sid)
    return f"{domain}\\{name}"


def list_user_permissions_windows(path):
    print(f"{'Dosya/Klasör':<60} {'Yetkili Kullanıcılar':<30} {'Yetkili Gruplar':<30}")
    print("=" * 120)

    for root, dirs, files in os.walk(path):
        for name in dirs + files:
            full_path = os.path.join(root, name)

            # Dosya türünü belirle
            file_type = "Klasör" if os.path.isdir(full_path) else "Dosya"

            # Dosya izinlerini al
            permissions = oct(stat.S_IMODE(os.lstat(full_path).st_mode))[2:]

            # Yetkili kullanıcıları ve grupları al (Windows)
            try:
                owner = get_owner_info(full_path)
                group = "Bilinmiyor"  # Windows'ta dosya grup bilgisi doğrudan alınamayabilir
            except Exception as e:
                owner, group = "Bilinmiyor", "Bilinmiyor"

            # Sonuçları yazdır
            print(f"{full_path:<60} {owner:<30} {group:<30}")


if __name__ == "__main__":
    # İzinleri listeleyeceğiniz dizini aşağıdaki gibi değiştirin.
    path_to_scan = r"\\file\Profile\username\Start Menu" # unc path or normal path

    list_user_permissions_windows(path_to_scan)
