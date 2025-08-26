from db.db_local import get_latest_mesures, mark_as_sent
from db.db_remote import insert_mesures


def sync_mesures():
    
    mesures = get_latest_mesures()
    if not mesures:
        print("Aucune mesure à synchroniser.")
        return

    print(f"===> {len(mesures)} mesures à envoyer...")

    # Envoyer vers le remote
    insert_mesures(mesures)

    # Marquer comme envoyées
    ids = [m['id'] for m in mesures]
    mark_as_sent(ids)

    print("Synchronisation terminée.")

if __name__ == "__main__":
    sync_mesures()
