# Modèles canoniques

Les sources éditables sont `diagrams/mcd.mmd`, `diagrams/mld.mmd` et `diagrams/mpd.mmd`. Le MPD exécutable est ordonné sous `sql/`. Les modèles décrivent les données ; ils ne définissent ni agrégat, ni value object, ni bounded context.

Rendu attendu lorsque Mermaid CLI est disponible :

```bash
mmdc -i diagrams/mcd.mmd -o diagrams/mcd.svg
mmdc -i diagrams/mld.mmd -o diagrams/mld.svg
mmdc -i diagrams/mpd.mmd -o diagrams/mpd.svg
```
