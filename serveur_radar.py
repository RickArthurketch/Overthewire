using System.Collections;
using UnityEngine;
using UnityEngine.Android;
using UnityEngine.UI;

[System.Serializable]
public class RadarData
{
    public float respiration;
}

public class RadarManager : MonoBehaviour
{
    private AndroidJavaObject bleBridge;
    public Text texteRespiration;
    public Transform sphereTransform;

    public float valeurCapteurMin = 5f;
    public float valeurCapteurMax = 40f;
    public float tailleBouleMin = 0.5f;
    public float tailleBouleMax = 2.5f;

    private float derniereValeur = 0f;
    private string debugMsg = "Démarrage...";

    void Start()
    {
        if (sphereTransform != null) sphereTransform.localScale = Vector3.one * tailleBouleMin;
        if (Application.platform == RuntimePlatform.Android) StartCoroutine(InitBluetooth());
    }

    private IEnumerator InitBluetooth()
    {
        debugMsg = "Vérification permissions...";

        if (!Permission.HasUserAuthorizedPermission("android.permission.BLUETOOTH_CONNECT") ||
            !Permission.HasUserAuthorizedPermission("android.permission.BLUETOOTH_SCAN"))
        {
            debugMsg = "Attente validation permissions...";
            Permission.RequestUserPermission("android.permission.BLUETOOTH_CONNECT");
            Permission.RequestUserPermission("android.permission.BLUETOOTH_SCAN");

            while (!Permission.HasUserAuthorizedPermission("android.permission.BLUETOOTH_CONNECT"))
            {
                yield return new WaitForSeconds(0.5f);
            }
        }

        debugMsg = "Permissions OK. Lancement Java...";
        try
        {
            bleBridge = new AndroidJavaObject("com.tonnom.vr.BLEBridge");
            bleBridge.Call("connectToRaspberry");
            debugMsg = "Recherche de la Raspberry...";
        }
        catch (System.Exception e)
        {
            debugMsg = "Erreur Java: " + e.Message;
        }
    }

    public void OnDataReceived(string jsonString)
    {
        try
        {
            RadarData data = JsonUtility.FromJson<RadarData>(jsonString);
            derniereValeur = data.respiration;
        }
        catch
        {
            debugMsg = "Erreur lecture JSON";
        }
    }

    void Update()
    {
        if (texteRespiration != null)
        {
            // Si on a des données, on affiche la valeur, sinon on affiche l'étape en cours
            if (derniereValeur > 0)
            {
                texteRespiration.text = "Respiration : " + derniereValeur.ToString("F1");
            }
            else
            {
                texteRespiration.text = debugMsg;
            }
        }

        if (sphereTransform != null && derniereValeur > 0)
        {
            float t = Mathf.InverseLerp(valeurCapteurMin, valeurCapteurMax, derniereValeur);
            float taille = Mathf.Lerp(tailleBouleMin, tailleBouleMax, t);
            sphereTransform.localScale = new Vector3(taille, taille, taille);
        }
    }

    public void OnJavaDebug(string message)
    {
        debugMsg = message;
    }

    void OnDestroy()
    {
        if (bleBridge != null) bleBridge.Call("disconnect");
    }
}
