using UnityEngine;
using TMPro;

public class SquatSimulator : MonoBehaviour
{
    public BreathingLightController lightController;
    public TextMeshProUGUI affichageTexte;

    [System.Serializable]
    public struct Etape
    {
        public float temps;
        public float hr; // Rythme cardiaque
        public float rr; // Respiration
    }

    // Le tableau des valeurs (Repos -> Squats -> R�cup�ration)
    public Etape[] scenario = new Etape[] {
        new Etape { temps = 0f, hr = 65f, rr = 14f },
        new Etape { temps = 15f, hr = 66f, rr = 14f },
        new Etape { temps = 30f, hr = 85f, rr = 22f },
        new Etape { temps = 45f, hr = 125f, rr = 30f },
        new Etape { temps = 60f, hr = 150f, rr = 36f },
        new Etape { temps = 75f, hr = 130f, rr = 28f },
        new Etape { temps = 90f, hr = 105f, rr = 22f },
        new Etape { temps = 110f, hr = 85f, rr = 18f },
        new Etape { temps = 130f, hr = 75f, rr = 15f },
        new Etape { temps = 150f, hr = 68f, rr = 14f }
    };

    private float chronometre = 0f;
    private float dureeTotale = 150f;

    void Update()
    {
        // Fait avancer le temps
        chronometre += Time.deltaTime;

        // Recommence � z�ro une fois le sc�nario termin�
        if (chronometre > dureeTotale) chronometre = 0f;

        // Cherche dans quelle phase on se trouve pour calculer les valeurs exactes
        for (int i = 0; i < scenario.Length - 1; i++)
        {
            if (chronometre >= scenario[i].temps && chronometre <= scenario[i + 1].temps)
            {
                float progression = (chronometre - scenario[i].temps) / (scenario[i + 1].temps - scenario[i].temps);

                float hrActuel = Mathf.Lerp(scenario[i].hr, scenario[i + 1].hr, progression);
                float rrActuel = Mathf.Lerp(scenario[i].rr, scenario[i + 1].rr, progression);

                // Envoie l'info � la lumi�re
                if (lightController != null)
                {
                    lightController.simulatedBreathingRate = rrActuel;
                }

                // Envoie l'info au texte
                if (affichageTexte != null)
                {
                    affichageTexte.text = $"Respiration : {rrActuel:F1} rpm\nCardiaque : {hrActuel:F1} bpm";
                }

                break;
            }
        }
    }
}
