package com.placement.model;

import jakarta.persistence.*;

@Entity
@Table(name = "students")
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    private double cgpa;
    private double aptitudeScore;
    private double codingScore;
    private double communicationScore;
    private double attendance;
    private int projects;
    private int internships;
    private int certifications;
    private int backlogs;
    private boolean placementStatus;

    public Student() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String value) { name = value; }
    public double getCgpa() { return cgpa; }
    public void setCgpa(double value) { cgpa = value; }
    public double getAptitudeScore() { return aptitudeScore; }
    public void setAptitudeScore(double value) { aptitudeScore = value; }
    public double getCodingScore() { return codingScore; }
    public void setCodingScore(double value) { codingScore = value; }
    public double getCommunicationScore() { return communicationScore; }
    public void setCommunicationScore(double value) { communicationScore = value; }
    public double getAttendance() { return attendance; }
    public void setAttendance(double value) { attendance = value; }
    public int getProjects() { return projects; }
    public void setProjects(int value) { projects = value; }
    public int getInternships() { return internships; }
    public void setInternships(int value) { internships = value; }
    public int getCertifications() { return certifications; }
    public void setCertifications(int value) { certifications = value; }
    public int getBacklogs() { return backlogs; }
    public void setBacklogs(int value) { backlogs = value; }
    public boolean isPlacementStatus() { return placementStatus; }
    public void setPlacementStatus(boolean value) { placementStatus = value; }
}
