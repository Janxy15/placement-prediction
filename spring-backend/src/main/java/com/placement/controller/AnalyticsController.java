package com.placement.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Map;

@RestController
@RequestMapping("/api/analytics")
@CrossOrigin(origins = "http://localhost:5173")
public class AnalyticsController {
    private final RestTemplate client = new RestTemplate();
    private final String url;

    public AnalyticsController(@Value("${python.analysis.url}") String url) {
        this.url = url;
    }

    @GetMapping("/overview")
    public ResponseEntity<?> overview() { return call("/analysis/overview"); }

    @GetMapping("/correlations")
    public ResponseEntity<?> correlations() { return call("/analysis/correlations"); }

    @GetMapping("/probabilities")
    public ResponseEntity<?> probabilities() { return call("/analysis/probabilities"); }

    @GetMapping("/hypothesis")
    public ResponseEntity<?> hypothesis() { return call("/analysis/hypothesis"); }

    private ResponseEntity<?> call(String path) {
        try {
            return ResponseEntity.ok(client.getForObject(url + path, Object.class));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", "Python service is not running."));
        }
    }
}
