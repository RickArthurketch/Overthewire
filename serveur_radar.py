using UnityEngine;

public class BreathingLightController : MonoBehaviour
{
    public Light directionalLight;

    [Header("Donn�es Radar")]
    public float simulatedBreathingRate = 15f;

    [Header("Seuils de Respiration")]
    public float seuilBas = 14f;  // Cal� sur la respiration au repos
    public float seuilHaut = 36f; // Cal� sur l'effort max des squats

    [Header("Rendu Visuel")]
    public float intensiteRepos = 0.5f;
    public float intensiteEffort = 2.5f;

    public Color couleurRepos = Color.white;
    public Color couleurEffort = new Color(1f, 0.8f, 0.6f); // Une teinte un peu plus chaude pour l'effort

    public float vitesseTransition = 3f;

    void Start()
    {
        if (directionalLight == null) directionalLight = GetComponent<Light>();
        directionalLight.type = LightType.Directional;
    }

    void Update()
    {
        // 1. D�termine o� on se situe entre le repos (0) et l'effort max (1)
        float pourcentageEffort = Mathf.InverseLerp(seuilBas, seuilHaut, simulatedBreathingRate);

        // 2. D�duit l'intensit� et la couleur exactes pour cet instant pr�cis
        float intensiteCible = Mathf.Lerp(intensiteRepos, intensiteEffort, pourcentageEffort);
        Color couleurCible = Color.Lerp(couleurRepos, couleurEffort, pourcentageEffort);

        // 3. Applique la modification en douceur pour �viter les saccades
        directionalLight.intensity = Mathf.Lerp(directionalLight.intensity, intensiteCible, Time.deltaTime * vitesseTransition);
        directionalLight.color = Color.Lerp(directionalLight.color, couleurCible, Time.deltaTime * vitesseTransition);
    }
}
