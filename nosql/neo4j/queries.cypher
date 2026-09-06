MATCH (p:Profile {id:'PRO-0001'}), (t:Training {status:'PUBLISHED'})-[r:REQUIRES]->(s:Skill)
OPTIONAL MATCH (p)-[h:HAS_SKILL]->(s)
WITH t, collect({skill:s.id, required:r.level, current:coalesce(h.level,0)}) AS explanation,
     sum(CASE WHEN coalesce(h.level,0) < r.level THEN r.level-coalesce(h.level,0) ELSE 0 END) AS gap
RETURN t.id AS trainingId, t.title AS title, gap, explanation
ORDER BY gap ASC, trainingId ASC LIMIT 10;

MATCH (t:Training)-[:REQUIRES]->(s:Skill)<-[:HAS_SKILL]-(p:Profile {id:'PRO-0001'})
RETURN t.id, collect(s.id) AS sharedSkills;
