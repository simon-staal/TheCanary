// Defines our database models for transfering
const mongoose = require('mongoose'); 
// Defining source schema
const historicalSchema = new mongoose.Schema({
    id: Number,
    data: Object,
    time: Date
});
  
// Defining destination schema
const archiveSchema = new mongoose.Schema({
    id: Number,
    data: Object,
    time: Date
});
  
// Creating model for both schemas
const Historical = mongoose.model('source', historicalSchema);
const Archive = mongoose.model(
    'destination', archiveSchema);

// Exporting our modals
module.exports = {
    Source: Historical, Destination: Archive
}