using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class BreathingLightController : MonoBehaviour
{
    [Header("Configuration Réseau")]
    public int port = 5005;

    [Header("Configuration Lumière")]
    public Light roomLight;
    public float minIntensity = 0.5f; // Luminosité minimum (ex: respiration lente)
    public float maxIntensity = 2.0f; // Luminosité maximum (ex: respiration rapide)

    [Header("Valeurs de Respiration Attendues")]
    public float minRespiration = 12f;
    public float maxRespiration = 25f;

    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = false;
    private float currentRespirationRate = 15f; // Valeur par défaut

    void Start()
    {
        // Si aucune lumière n'est assignée, on cherche celle sur le même objet
        if (roomLight == null)
        {
            roomLight = GetComponent<Light>();
        }

        StartNetworkListener();
    }

    private void StartNetworkListener()
    {
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true; // Permet de fermer le thread quand Unity s'arrête
        isRunning = true;
        receiveThread.Start();
        Debug.Log($"Écoute UDP démarrée sur le port {port}");
    }

    private void ReceiveData()
    {
        udpClient = new UdpClient(port);
        IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);

        while (isRunning)
        {
            try
            {
                // Bloque jusqu'à recevoir une donnée
                byte[] data = udpClient.Receive(ref anyIP);
                string text = Encoding.UTF8.GetString(data);

                // Convertit le texte reçu en nombre flottant
                if (float.TryParse(text, System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out float rate))
                {
                    currentRespirationRate = rate;
                }
            }
            catch (System.Exception e)
            {
                if (isRunning) Debug.LogError("Erreur UDP : " + e.Message);
            }
        }
    }

    void Update()
    {
        if (roomLight == null) return;

        // On calcule le pourcentage de la fréquence respiratoire par rapport à nos bornes
        float t = Mathf.InverseLerp(minRespiration, maxRespiration, currentRespirationRate);

        // On détermine la luminosité cible en fonction de ce pourcentage
        float targetIntensity = Mathf.Lerp(minIntensity, maxIntensity, t);

        // Transition douce de la luminosité actuelle vers la luminosité cible
        roomLight.intensity = Mathf.Lerp(roomLight.intensity, targetIntensity, Time.deltaTime * 3f);
    }

    void OnApplicationQuit()
    {
        // Nettoyage propre à la fermeture
        isRunning = false;
        if (udpClient != null) udpClient.Close();
        if (receiveThread != null && receiveThread.IsAlive) receiveThread.Abort();
    }
}
