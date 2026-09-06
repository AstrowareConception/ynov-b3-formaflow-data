db = db.getSiblingDB("formaflow_catalog");
db.training_catalog.drop();
db.createCollection("training_catalog", {
  validator: {$jsonSchema: {
    bsonType: "object",
    required: ["_id", "slug", "title", "status", "attributes", "skills", "nextSessionIds", "projectedAt", "sourceVersion"],
    properties: {
      _id: {bsonType: "string"},
      slug: {bsonType: "string"},
      title: {bsonType: "string"},
      status: {enum: ["DRAFT", "PUBLISHED", "ARCHIVED"]},
      attributes: {bsonType: "object"},
      skills: {bsonType: "array", maxItems: 30},
      modules: {bsonType: "array", maxItems: 50},
      nextSessionIds: {bsonType: "array", maxItems: 3},
      projectedAt: {bsonType: "date"},
      sourceVersion: {bsonType: "int", minimum: 1}
    }
  }}
});
db.training_catalog.createIndex({slug: 1}, {unique: true, name: "uq_training_slug"});
db.training_catalog.createIndex({status: 1, "skills.code": 1}, {name: "idx_published_skill"});
db.training_catalog.createIndex({"attributes.level": 1}, {name: "idx_level", partialFilterExpression: {status: "PUBLISHED"}});
db.training_catalog.insertMany([
  {
    _id: "TRN-0001", slug: "concevoir-api-robuste", title: "Concevoir une API robuste", status: "PUBLISHED",
    summary: "Formation synthétique sur les contrats API.",
    attributes: {level: "INTERMEDIATE", deliveryModes: ["ONSITE"], language: "fr", labIncluded: true},
    skills: [{code: "SKL-002", label: "Conception API", targetLevel: 2}],
    modules: [{code: "MOD-API-01", title: "Contrats", minutes: 120}],
    nextSessionIds: ["SES-2027-0001"], projectedAt: ISODate("2027-01-20T12:00:00Z"), sourceVersion: NumberInt(1)
  },
  {
    _id: "TRN-0002", slug: "modeliser-donnees-metier", title: "Modéliser des données métier", status: "PUBLISHED",
    summary: "Formation synthétique sur les modèles de données.",
    attributes: {level: "INTERMEDIATE", deliveryModes: ["ONSITE", "REMOTE"], language: "fr"},
    skills: [{code: "SKL-001", label: "Modélisation de données", targetLevel: 2}],
    modules: [{code: "MOD-DATA-01", title: "Dépendances fonctionnelles", minutes: 90}],
    nextSessionIds: ["SES-2027-0002"], projectedAt: ISODate("2027-01-20T12:00:00Z"), sourceVersion: NumberInt(1)
  },
  {
    _id: "TRN-0003", slug: "securiser-application-web", title: "Sécuriser une application web", status: "ARCHIVED",
    attributes: {level: "ADVANCED", language: "fr"},
    skills: [{code: "SKL-003", label: "Sécurité web", targetLevel: 3}],
    modules: [], nextSessionIds: [], projectedAt: ISODate("2027-01-20T12:00:00Z"), sourceVersion: NumberInt(1)
  }
]);
printjson({profile: "mongodb", count: db.training_catalog.countDocuments({}), slugLookup: db.training_catalog.countDocuments({slug: "modeliser-donnees-metier"})});
