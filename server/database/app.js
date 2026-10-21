const express = require("express");
const mongoose = require("mongoose");
const fs = require("fs");
const cors = require("cors");
const app = express();
const port = 3030;

app.use(cors());
app.use(express.json());

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", "utf8"));
const dealerships_data = JSON.parse(
  fs.readFileSync("dealerships.json", "utf8"),
);

mongoose.connect("mongodb://mongo_db:27017/", { dbName: "dealershipsDB" });

const Reviews = require("./review");
const Dealerships = require("./dealership");

app.get("/", (req, res) => {
  res.send("Welcome to the Mongoose API");
});

app.get("/fetchDealers", async (req, res) => {
  try {
    const dealers = await Dealerships.find();
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ error: "Error fetching dealers" });
  }
});

app.get("/fetchDealers/:state", async (req, res) => {
  try {
    const dealers = await Dealerships.find({ state: req.params.state });
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ error: "Error fetching dealers by state" });
  }
});

app.get("/fetchDealer/:id", async (req, res) => {
  try {
    const dealer = await Dealerships.find({ id: req.params.id });
    if (dealer.length > 0) {
      res.json(dealer);
    } else {
      res.status(404).json({ error: "Dealer not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Error fetching dealer" });
  }
});

app.get("/fetchReviews/dealer/:id", async (req, res) => {
  try {
    const reviews = await Reviews.find({ dealership: req.params.id });
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ error: "Error fetching reviews" });
  }
});

app.post("/insert_review", async (req, res) => {
  try {
    const newReview = new Reviews(req.body);
    const savedReview = await newReview.save();
    res.status(201).json(savedReview);
  } catch (error) {
    res.status(500).json({ error: "Error inserting review" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
