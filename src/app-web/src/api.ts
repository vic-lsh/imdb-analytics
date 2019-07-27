const env = process.env.NODE_ENV

/** 
 * Database URL getter.
 * @returns the base URL for the database service, depending on the environment.
 */
export const DB_SERVICE_BASE_URL = (() => {
  return (env === 'development' || env === 'test') ?
    'http://localhost:8001' :
    'https://imdb-analytics.azurewebsites.net/'
})()

/** 
 * Job Service URL. 
 * 
 * The job service is responsible for creating and 
 * completing data extraction jobs. Schedule a job if some information is 
 * queried but does not exist on the database.
 * 
 * @returns the base URL for the Job Service, depending on the environment.
 */
export const JOB_SERVICE_BASE_URL = (() => {
  return (env === 'development' || env === 'test') ?
    'http://localhost:3778' :
    'https://job-service'
})()
