db = db.getSiblingDB("formaflow_catalog");
db.training_catalog.findOne({slug: "modeliser-donnees-metier"});
db.training_catalog.find({status: "PUBLISHED", "skills.code": "SKL-001"}, {_id: 1, title: 1, skills: 1}).sort({title: 1});
db.training_catalog.find({status: "PUBLISHED", "attributes.level": "INTERMEDIATE"}, {_id: 1, title: 1});
db.training_catalog.getIndexes();
