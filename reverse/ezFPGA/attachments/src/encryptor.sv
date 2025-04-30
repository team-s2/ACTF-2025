module Encryptor#(
    parameter logic [7:0] FLAG [0:13] = {
        "A", "C", "T", "F", "{", "t", "e", "s", "t", "f", "l", "a", "g", "}"
    }
)(
    input rst,
    input clk,
    output logic [7:0] cypher
);

    typedef logic [7:0] uint8_t;
    localparam l = $size(FLAG);

    uint8_t aa [38:0];

    genvar i;
    generate
        for(i = 0; i < l; i++) begin : gen
            assign aa[i] = FLAG[i];
        end
        for (i = l; i < 39; i++) begin : gen
            assign aa[i] = 0;
        end
    endgenerate

    uint8_t ab [0:3] = {11,4,5,14};
    uint8_t ac [35:0];

    generate
        for(i = 0; i < 36; i++) begin : gen
            assign ac[i] = aa[i]*ab[0] + aa[i+1]*ab[1] + aa[i+2]*ab[2] + aa[i+3]*ab[3];
        end
    endgenerate

    uint8_t ad [0:35] = {116,174,193,124,102,100,11,193,115,4,127,139,98,214,197,145,97,151,31,30,117,15,230,179,235,25,244,202,73,222,15,191,119,140,94,32};
    
    uint8_t ae [35:0];

    generate
        for (i = 0; i < 36; i = i + 1) begin
            assign ae[i] = ac[i/6*6]*ad[i%6]+ac[i/6*6+1]*ad[i%6+6]+ac[i/6*6+2]*ad[i%6+12]+ac[i/6*6+3]*ad[i%6+18]+ac[i/6*6+4]*ad[i%6+24]+ac[i/6*6+5]*ad[i%6+30];
        end
    endgenerate

    uint8_t af[35:0];
    uint8_t ba[255:0];
    uint8_t ca,cb,cd,ce,cf,cg,ch;
    uint8_t da;
    uint8_t db[0:7] = {"e","c","l","i","p","s","k","y"};
    typedef enum logic[1:0] {S0,S1,S2,S3} state_t;
    state_t state;

    assign cd = ca + 1;
    assign ce = cb + ba[cd];
    assign cf = ba[cd] + ba[ce];
    assign ch = cg + ba[da] + db[da%8];

    always_ff @( posedge clk or posedge rst) begin
        if (rst) begin
            ca <= 0;
            cb <= 0;
            cg <= 0;
            da <= 0;
            cypher <= 0;
            state <= S1;
        end else begin
            case (state)
                S0: begin
                    if (da != 8'd255) begin
                        ba[da] <= da;
                        da <= da + 1;
                    end else begin
                        ba[da] <= da;
                        da <= 0;
                        state <= S1;
                    end
                end
                S1: begin
                    if (da != 8'd255) begin
                        ba[da] <= ba[ch];
                        ba[ch] <= ba[da];
                        cg <= ch;
                        da <= da + 1;
                    end else begin
                        ba[da] <= ba[ch];
                        ba[ch] <= ba[da];
                        da <= 0;
                        state <= S2;
                    end
                end
                S2: begin
                    if (da < 36) begin
                        ba[cd] <= ba[ce];
                        ba[ce] <= ba[cd];
                        af[da[5:0]] <= ba[cf] + ae[da[5:0]];
                        ca <= cd;
                        cb <= ce;
                        da <= da + 1;
                    end else begin
                        da <= 0;
                        state <= S3;
                    end
                end
                S3: begin
                    if (da < 36) begin
                        cypher <= af[da[5:0]];
                        da <= da + 1;
                    end else begin
                        cypher <= 0;
                    end
                end
            endcase
        end
    end




endmodule