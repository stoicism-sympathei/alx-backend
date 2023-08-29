import { createClient } from 'redis';
import { promisify } from 'util';
import express, { json } from 'express';
import kue from 'kue';

// Redis Client
const client = createClient();
const getAsync = promisify(client.get).bind(client);

// Kue Queue
const queue = kue.createQueue();

// Express Server
const app = express();

// Functions
const reserveSeat = (number) => {
  client.set('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  return await getAsync('available_seats');
};

// App initialization
reserveSeat(50);
let reservationEnabled = true;

app.get('/available_seats', async (req, res) => {
  res.json({ numberOfAvailableSeats: await getCurrentAvailableSeats() });
});

app.get('/reserve_seat', (req, res) => {
  if (reservationEnabled) {
    const job = queue.create('reserve_seat').save((error) => {
      if (error) {
        res.json({ status: 'Reservation failed' });
      } else {
        res.json({ status: 'Reservation in process' });
      }
    });

    job
      .on('complete', (result) =>
        console.log(`Seat reservation job ${job.id} completed`),
      )
      .on('failed', (error) => {
        console.error(`Seat reservation job ${job.id} failed: ${error}`);
      });
  } else {
    res.json({ status: 'Reservation are blocked' });
  }
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    reserveSeat((await getCurrentAvailableSeats()) - 1);
    console.log(await getCurrentAvailableSeats(), reservationEnabled);
    if ((await getCurrentAvailableSeats()) <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    done();
  });
});

app.listen(1245);
