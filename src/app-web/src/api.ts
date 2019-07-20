const env = process.env.NODE_ENV

/** 
 * Database URL getter.
 * @returns the base URL for the database service, depending on the environment.
 */
export const DB_SERVICE_BASE_URL = (() => {
  return (env === 'development' || env === 'test') ?
    'http://localhost:8001' :
    'https://db-service'
})()
