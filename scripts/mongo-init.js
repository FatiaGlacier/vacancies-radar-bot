const appUser = _getEnv('MONGO_APP_USER')
const appPassword = _getEnv('MONGO_APP_PASSWORD')
const appDB = _getEnv('MONGO_APP_DB')

db = db.getSiblingDB(appDB);

db.createUser({
  user: appUser,
  pwd: appPassword,
  roles: [{ role: 'readWrite', db: 'mybot_db' }]
});

print('✅ Created user: ' + appUser);