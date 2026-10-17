package com.placement.controller;

import com.placement.model.Student;
import com.placement.repository.StudentRepository;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/students")
@CrossOrigin(origins = "http://localhost:5173")
public class StudentController {
    private final StudentRepository repository;

    public StudentController(StudentRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<Student> getAll() {
        return repository.findAll();
    }

    @PostMapping
    public Student create(@RequestBody Student student) {
        student.setId(null);
        return repository.save(student);
    }
}
