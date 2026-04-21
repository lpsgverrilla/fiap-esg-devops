// Seed script executed automatically by MongoDB on first boot.
// Docker-entrypoint mounts /docker-entrypoint-initdb.d/ and runs *.js via mongosh
// against the database named by MONGO_INITDB_DATABASE.
// Based on the original academic script "Monitoramento de Emissoes de Carbono".

print("[seed] Inserindo dados ESG iniciais em " + db.getName());

db.createCollection("empresas");
db.empresas.insertMany([
  { nome: "EcoLog Transportes", setor: "Logistica",     pais: "Brasil",    ano_fundacao: 2008 },
  { nome: "GreenTech Energia",  setor: "Energia",       pais: "Brasil",    ano_fundacao: 2012 },
  { nome: "SolarWave",          setor: "Energia Solar", pais: "Chile",     ano_fundacao: 2015 },
  { nome: "BioFood",            setor: "Alimentos",     pais: "Argentina", ano_fundacao: 2010 },
  { nome: "UrbanMob",           setor: "Mobilidade",    pais: "Brasil",    ano_fundacao: 2018 },
  { nome: "CleanWater",         setor: "Saneamento",    pais: "Peru",      ano_fundacao: 2011 },
  { nome: "EcoBuild",           setor: "Construcao",    pais: "Colombia",  ano_fundacao: 2006 },
  { nome: "AgroLife",           setor: "Agronegocio",   pais: "Brasil",    ano_fundacao: 2009 },
  { nome: "WindPower",          setor: "Energia Eolica",pais: "Uruguai",   ano_fundacao: 2014 },
  { nome: "RecycleX",           setor: "Reciclagem",    pais: "Brasil",    ano_fundacao: 2016 }
]);

db.createCollection("emissoes");
db.emissoes.insertMany([
  { empresa: "EcoLog Transportes", ano: 2025, emissao_CO2_ton: 1200, diesel_litros: 500000, energia_renovavel_percentual: 25 },
  { empresa: "GreenTech Energia",  ano: 2025, emissao_CO2_ton: 300,  energia_renovavel_percentual: 85 },
  { empresa: "SolarWave",          ano: 2025, emissao_CO2_ton: 150,  paineis_solares_instalados: 12000 },
  { empresa: "BioFood",            ano: 2025, emissao_CO2_ton: 800,  residuos_organicos_ton: 400 },
  { empresa: "UrbanMob",           ano: 2025, emissao_CO2_ton: 500,  frota_eletrica_percentual: 40 },
  { empresa: "CleanWater",         ano: 2025, emissao_CO2_ton: 200,  agua_tratada_m3: 150000 },
  { empresa: "EcoBuild",           ano: 2025, emissao_CO2_ton: 950,  materiais_reciclados_percentual: 25 },
  { empresa: "AgroLife",           ano: 2025, emissao_CO2_ton: 1100, area_reflorestada_hectares: 80 },
  { empresa: "WindPower",          ano: 2025, emissao_CO2_ton: 100,  turbinas_ativas: 45 },
  { empresa: "RecycleX",           ano: 2025, emissao_CO2_ton: 250,  creditos_carbono: 300 }
]);

db.createCollection("impacto_social");
db.impacto_social.insertMany([
  { empresa: "EcoLog Transportes", ano: 2025, funcionarios_total: 320, mulheres_percentual: 35, investimento_social_mil: 150 },
  { empresa: "GreenTech Energia",  ano: 2025, funcionarios_total: 180, mulheres_percentual: 42, programa_comunidade: "Educacao Ambiental" },
  { empresa: "SolarWave",          ano: 2025, funcionarios_total: 95,  diversidade_percentual: 28 },
  { empresa: "BioFood",            ano: 2025, funcionarios_total: 410, investimento_social_mil: 220 },
  { empresa: "UrbanMob",           ano: 2025, funcionarios_total: 150, programa_comunidade: "Mobilidade Sustentavel" },
  { empresa: "CleanWater",         ano: 2025, funcionarios_total: 210, projetos_sociais: ["Agua para Todos", "Saneamento Rural"] },
  { empresa: "EcoBuild",           ano: 2025, funcionarios_total: 500, mulheres_percentual: 38 },
  { empresa: "AgroLife",           ano: 2025, funcionarios_total: 380, diversidade_percentual: 22 },
  { empresa: "WindPower",          ano: 2025, funcionarios_total: 120, investimento_social_mil: 90 },
  { empresa: "RecycleX",           ano: 2025, funcionarios_total: 75,  programa_comunidade: "Reciclagem nas Escolas" }
]);

db.createCollection("governanca");
db.governanca.insertMany([
  { empresa: "EcoLog Transportes", ano: 2025, auditoria: { tipo: "Externa", empresa_auditora: "SGS", resultado: "Aprovado" }, conselho_membros: 5 },
  { empresa: "GreenTech Energia",  ano: 2025, auditoria: { tipo: "Interna", resultado: "Aprovado com ressalvas" }, codigo_etica: true },
  { empresa: "SolarWave",          ano: 2025, compliance_score: 88 },
  { empresa: "BioFood",            ano: 2025, auditoria: { tipo: "Externa", empresa_auditora: "Bureau Veritas", resultado: "Aprovado" } },
  { empresa: "UrbanMob",           ano: 2025, codigo_etica: true, canal_denuncia: true },
  { empresa: "CleanWater",         ano: 2025, compliance_score: 91 },
  { empresa: "EcoBuild",           ano: 2025, auditoria: { tipo: "Interna", resultado: "Aprovado apos revisao" } },
  { empresa: "AgroLife",           ano: 2025, conselho_membros: 7 },
  { empresa: "WindPower",          ano: 2025, codigo_etica: true },
  { empresa: "RecycleX",           ano: 2025, compliance_score: 95 }
]);

db.createCollection("metas_sustentabilidade");
db.metas_sustentabilidade.insertMany([
  { empresa: "EcoLog Transportes", meta: "Reduzir 20% das emissoes de CO2",        prazo_ate: 2030, status: "Em andamento" },
  { empresa: "GreenTech Energia",  meta: "100% energia renovavel",                  prazo_ate: 2028, status: "Quase concluido" },
  { empresa: "SolarWave",          meta: "Neutralidade de carbono",                 prazo_ate: 2035, status: "Planejamento" },
  { empresa: "BioFood",            meta: "Reducao de residuos organicos em 30%",   prazo_ate: 2027, status: "Em andamento" },
  { empresa: "UrbanMob",           meta: "Frota 70% eletrica",                      prazo_ate: 2032, status: "Planejamento" },
  { empresa: "CleanWater",         meta: "Reuso de 50% da agua tratada",            prazo_ate: 2029, status: "Em andamento" },
  { empresa: "EcoBuild",           meta: "Uso de 40% materiais reciclados",         prazo_ate: 2030, status: "Em andamento" },
  { empresa: "AgroLife",           meta: "Reflorestamento de 200 hectares",         prazo_ate: 2033, status: "Planejamento" },
  { empresa: "WindPower",          meta: "Dobrar capacidade de energia limpa",      prazo_ate: 2031, status: "Em andamento" },
  { empresa: "RecycleX",           meta: "Aumentar reciclagem em 50%",              prazo_ate: 2026, status: "Concluido" }
]);

print("[seed] Concluido. Collections: " + db.getCollectionNames().join(", "));
