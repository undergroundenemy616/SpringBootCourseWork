package main.exception;

public class InvalidJwtAuthenicationException extends RuntimeException{
    public InvalidJwtAuthenicationException(String message) {
        super(message);
    }
}
