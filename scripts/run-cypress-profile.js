const profile = process.argv[2];

if (!profile) {
  console.error('Usage: node scripts/run-cypress-profile.js <profile>');
  process.exit(1);
}

process.env.CYPRESS_PROFILE_MODE = profile;
require('./run-cypress');
