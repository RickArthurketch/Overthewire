using UnityEngine;

public class LightController : MonoBehaviour
{
    public Light lumiere;

    [Header("Limites de respiration")]
    public float seuilBas = 12f;
    public float seuilHaut = 25f;

    [Header("Intensités lumineuses")]
    public float intensiteMin = 0.2f; // Pièce sombre si respiration lente
    public float intensiteMax = 2.0f; // Pièce très claire si respiration rapide
    
    public float vitesseTransition = 2f;

    private float respirationActuelle = 15f;

    void Start()
    {
        if (lumiere == null) lumiere = GetComponent<Light>();
    }

    public void MettreAJourRespiration(float nouvelleValeur)
    {
        respirationActuelle = nouvelleValeur;
    }

    void Update()
    {
        // Calcule le pourcentage d'effort entre le seuil bas et haut
        float pourcentage = Mathf.InverseLerp(seuilBas, seuilHaut, respirationActuelle);
        
        // Déduit l'intensité correspondante
        float intensiteCible = Mathf.Lerp(intensiteMin, intensiteMax, pourcentage);

        // Applique le changement en douceur
        lumiere.intensity = Mathf.Lerp(lumiere.intensity, intensiteCible, Time.deltaTime * vitesseTransition);
    }
}
