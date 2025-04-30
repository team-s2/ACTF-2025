`timescale 1ns/1ps
module Testbench(
    output logic [7:0] cypher
);

    logic rst;
    logic clk;

    Encryptor dut(
        .rst(rst),
        .clk(clk),
        .cypher(cypher)
    );

    initial begin
        clk = 1'b0;
        rst = 1'b1;
        #10;
        rst = 1'b0;
    end

    always begin
        clk = ~clk;
        #5;
    end

    reg [31:0] cycle_count = 0;
    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
        if (cycle_count >= 1000) begin
            $display("Reached max cycle count %d", cycle_count);
            $finish;
        end
    end

    always begin
        if (cypher != 0) begin
            $display("%02x", cypher);
        end
    end

    initial begin
        $dumpfile("../Testbench.vcd");
        $dumpvars(0,dut);
        $dumpon;
    end
        
endmodule