# core

This folder contains class definitions and modules to be shared across components

## Article

Article objects represent parsed site articles with opinions on certain stocks at certain times

The Article class contains the following:

- tickers: list of relevant stocks
- author: Person that wrote the article
- date: Date of publication
- site: Site of origin
- url: URL of origin
- text: Body of the article

## Sentiment

Sentiment objects represent opinions about tickers from certain Sources at a certain time

## Source

A Source is a combination of site and author, such that credibility can be determined for an individual author or an entire site.