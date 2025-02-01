using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using MathNet.Numerics;
using AindBehaviorWaterTuner.DataTypes;
using System.Collections.Generic;

[Combinator]
[Description("Computes a water calibration model from a sequence of measurements.")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class WaterCalibrationModel
{
    public IObservable<WaterValveCalibration> Process(IObservable<IEnumerable<Measurement>> source)
    {
        return source.Select(value => {

            var input = new WaterValveCalibrationInput(){
                Measurements = value.ToList()
            };


            var delays = value.Select(x => x.ValveOpenTime).ToArray();
            var weights = value.Select(x => x.WaterWeight.Average()).ToArray();
            var p = Fit.Line(delays, weights);

            var output = new WaterValveCalibrationOutput(){
                Offset = p.Item1,
                Slope = p.Item2,
                R2 = GoodnessOfFit.RSquared(delays.Select(x => p.Item1+p.Item2*x), weights),
                IntervalAverage = value.ToDictionary(k => k.ValveOpenTime.ToString("0.0000"), v => v.WaterWeight.Average()),
                ValidDomain = delays.ToList()
            };

            return new WaterValveCalibration(){
                Input = input,
                Output = output,
                Date = DateTimeOffset.Now,
            };
        });
    }
}

public class LinearRegressionFit{
    public double Intercept { get; set; }
    public double Slope { get; set; }
    public double R2 { get; set; }
}
