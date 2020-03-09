# BERT_hate_speech_app
master thesis: creating a streaming and analytics application for automated hate speech detection

Kann BERT - ein ?state of the art language model for NLP?- helfen Hass auf Twitter zu erkennen? Sind solche Modelle praxistauglich und erkennen sie zuverlässig Hasskommentare? Können sie ohne grossen Aufwand in Streaming- und Analyseumgebungen eingebaut werden? Auch wenn eine Firma nicht über die Ressourcen wie Google oder Facebook verfügt? Diese und andere Fragen bezüglich der technischen Machbarkeit beantwortet diese Masterarbeit.

Die Struktur dieses Repos:
<ul>
<li>01_notebooks: alle jupyter notebooks um die Daten zu bereinigen, BERT Modelle zu trainieren und validieren</li>
<li>02_pipelines: streamsets pipelines um Tweets zu beziehen, zu klassifizieren und in elaticsearch zu speichern</li>
<li>03_elastic_create_index: postman Befehle um elasticsearch index und mapping zu erstellen </li>
<li>04_dashboard: Kibana Dashboard</li>
<li> 
05_flask_app: Flask App, welche auf http://nhex:12346/predict_bert deployed ist. Nur im privaten Netzwerk zu erreichen</li>
<li>06_k8s_deployment: Angepasste Kubernetes Deployments für den nHex</li>
</ul>



 

