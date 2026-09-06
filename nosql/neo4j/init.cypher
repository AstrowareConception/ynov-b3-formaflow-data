CREATE CONSTRAINT training_id_unique IF NOT EXISTS FOR (n:Training) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT skill_id_unique IF NOT EXISTS FOR (n:Skill) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT profile_id_unique IF NOT EXISTS FOR (n:Profile) REQUIRE n.id IS UNIQUE;
MATCH (n) DETACH DELETE n;

CREATE (t1:Training {id:'TRN-0001', title:'Concevoir une API robuste', status:'PUBLISHED', projectedAt:datetime('2027-01-20T12:00:00Z')}),
       (t2:Training {id:'TRN-0002', title:'Modéliser des données métier', status:'PUBLISHED', projectedAt:datetime('2027-01-20T12:00:00Z')}),
       (t3:Training {id:'TRN-0003', title:'Sécuriser une application web', status:'ARCHIVED', projectedAt:datetime('2027-01-20T12:00:00Z')}),
       (s1:Skill {id:'SKL-001', label:'Modélisation de données'}),
       (s2:Skill {id:'SKL-002', label:'Conception API'}),
       (s3:Skill {id:'SKL-003', label:'Sécurité web'}),
       (p1:Profile {id:'PRO-0001'}),
       (t1)-[:REQUIRES {level:2}]->(s2),
       (t2)-[:REQUIRES {level:2}]->(s1),
       (t3)-[:REQUIRES {level:3}]->(s3),
       (p1)-[:HAS_SKILL {level:1}]->(s1);

MATCH (p:Profile {id:'PRO-0001'}), (t:Training)-[r:REQUIRES]->(s:Skill)
OPTIONAL MATCH (p)-[h:HAS_SKILL]->(s)
WITH t, sum(CASE WHEN coalesce(h.level,0) < r.level THEN r.level-coalesce(h.level,0) ELSE 0 END) AS gap
RETURN t.id AS trainingId, gap ORDER BY gap ASC, trainingId ASC;
