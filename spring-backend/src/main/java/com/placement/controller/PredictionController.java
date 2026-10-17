package com.placement.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Map;

@RestController
@RequestMapping("/api/predict")
@CrossOrigin(origins = "http://localhost:5173")
public class PredictionController {
    private final RestTemplate client = new RestTemplate();
    private final String url;

    public PredictionController(@Value("${python.analysis.url}") String url) {
        this.url = url;
    }

    @PostMapping
    public ResponseEntity<?> predict(@RequestBody Map<String, Object> payload) {
        try {
            return ResponseEntity.ok(
                    client.postForObject(url + "/predict", payload, Object.class)
            );
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", "Python service is not running."));
        }
    }
}
