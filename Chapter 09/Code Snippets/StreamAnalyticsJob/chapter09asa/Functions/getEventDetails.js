function main(date_utc, time_utc, temp_f) {
  //get details object from input payload

  var event_details = {};
  event_details.date_utc = date_utc;
  event_details.time_utc = time_utc;
  event_details.temp_f = temp_f;

  return event_details;
}