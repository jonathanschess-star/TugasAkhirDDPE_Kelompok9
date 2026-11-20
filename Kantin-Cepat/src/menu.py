from dataclasses import dataclass


@dataclass(frozen=True)
class MenuItem:
    name: str
    price: int
    spicy: bool
    description: str
    image: str


MENU = [
    MenuItem("Nasi goreng kampung", 15000, True, "Nasi gurih, telur, dan sambal khas.", "nasi_goreng.svg"),
    MenuItem("Mie ayam", 13000, False, "Mie kenyal dengan ayam berbumbu dan sayur.", "mie_ayam.svg"),
    MenuItem("Soto ayam", 16000, False, "Kuah hangat, ayam suwir, dan nasi.", "soto_ayam.svg"),
    MenuItem("Bakso urat", 14000, True, "Bakso kenyal dengan kuah dan sambal.", "bakso.svg"),
    MenuItem("Ayam geprek", 18000, True, "Ayam renyah dengan sambal yang bisa diatur.", "ayam_geprek.svg"),
    MenuItem("Gado-gado", 12000, False, "Sayuran segar dengan saus kacang.", "gado_gado.svg"),
    MenuItem("Nasi ayam kecap", 17000, False, "Ayam kecap manis dengan nasi hangat.", "nasi_ayam.svg"),
    MenuItem("Mie goreng pedas", 15000, True, "Mie goreng berbumbu dengan rasa pedas.", "mie_goreng.svg"),
]


def recommend(budget: int, preference: str) -> tuple[list[MenuItem], bool]:
    affordable = [item for item in MENU if item.price <= budget]
    if preference == "Pedas":
        matched = [item for item in affordable if item.spicy]
    elif preference == "Tidak pedas":
        matched = [item for item in affordable if not item.spicy]
    else:
        matched = affordable

    fallback = not matched and bool(affordable) and preference != "Bebas"
    options = matched if matched else affordable
    options.sort(key=lambda item: (item.price, item.name))
    return options[:3], fallback
