
import redis from 'redis/dist/index';

// Create a Redis client
const client = redis.createClient(); 
// By default redis.createClient() will use 127.0.0.1 and port 6379

// Listen for the 'connect' event to see whether we successfully connected to the Redis server
client.on('connect', () => {
  console.log('Redis client connected to the server');
  // You can also perform other operations here after a successful connection
});

// Listen for the 'error' event to check if we failed to connect to the Redis server
client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

