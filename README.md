# BERT_hate_speech_app
master thesis: creating a streaming and analytics application for automated hate speech detection

Kann BERT - ein ?state of the art language model for NLP?- helfen Hass auf Twitter zu erkennen? Sind solche Modelle praxistauglich und erkennen sie zuverlässig Hasskommentare? Können sie ohne grossen Aufwand in Streaming- und Analyseumgebungen eingebaut werden? Auch wenn eine Firma nicht über die Ressourcen wie Google oder Facebook verfügt? Diese und andere Fragen bezüglich der technischen Machbarkeit beantwortet diese Masterarbeit.

Die Struktur dieses Repos:
<ul>
<li>01_notebooks: alle jupyter notebooks um die Daten zu bereinigen, BERT Modelle zu trainieren und validieren</li>
<li>02_pipelines: StreamSets pipelines um Tweets zu beziehen, zu klassifizieren und in elaticsearch zu speichern</li>
<li>03_elastic_create_index: Postman Befehle um Elasticsearch index und mapping zu erstellen </li>
<li>04_dashboard: Kibana Dashboard</li>
<li> 
05_flask_app: Flask App, welche auf den nHex deployed ist. Nur im privaten Netzwerk zu erreichen</li>
<li>06_k8s_deployment: Angepasste Kubernetes Deployments für den nHex</li>
</ul>

 BERT Hate Speech Detection (Zugriff via VPN): http://nhex:12346/predict_bert <br />
 LR, MNB, LSVC und LTSM Hate Speech Detechtion (Zugriff extern): http://www.detect-hate.com (hierbei werden andere Modelle verwendet.)


 

