module alu (
    input wire [7:0] a,
    input wire [7:0] b,
    input wire [2:0] op,
    output reg [7:0] result
);
always @(*) begin
    case(op)
        3'b000: result = a + b;
        3'b001: result = a - b;
        3'b010: result = a & b;
        3'b011: result = a | b;
        3'b100: result = a ^ b;
        3'b101: result = (a < b) ? 8'b1 : 8'b0;
        default: result = 8'b0;
    endcase
end
endmodule
