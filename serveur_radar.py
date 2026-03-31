private void ReceiveData()
{
    udpClient = new UdpClient(port);
    IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, port);

    while (isRunning)
    {
        try
        {
            byte[] data = udpClient.Receive(ref anyIP);
            string jsonString = Encoding.UTF8.GetString(data);
            
            // CETTE LIGNE VA TOUT NOUS DIRE
            Debug.Log("Message reçu de la Raspberry : " + jsonString);
            
            DonneesRadar radarData = JsonUtility.FromJson<DonneesRadar>(jsonString);

            if (!float.IsNaN(radarData.rr))
            {
                derniereRespiration = radarData.rr;
                nouvelleDonnee = true;
            }
        }
        catch (System.Exception) {}
    }
}
